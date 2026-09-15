"""Select the adaptive uncertainty threshold on validation, then freeze and evaluate."""
from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path
import sys
import time

import joblib
import numpy as np
import onnxruntime as ort
from sklearn.metrics import accuracy_score, confusion_matrix, f1_score, precision_recall_fscore_support
from tokenizers import Tokenizer

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))


def read_tsv(name: str) -> tuple[list[str], np.ndarray]:
    rows = (ROOT / f"data/processed/uci_sms/{name}.tsv").read_text(encoding="utf-8").splitlines()[1:]
    return [r.split("\t", 1)[1] for r in rows], np.asarray([int(r.split("\t", 1)[0]) for r in rows])


def metric(y: np.ndarray, p: np.ndarray, escalated: np.ndarray | None = None) -> dict:
    pred = p >= .5; tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    precision, recall, f1, _ = precision_recall_fscore_support(y, pred, average="binary", zero_division=0)
    result = {"n": len(y), "accuracy": float(accuracy_score(y, pred)), "precision": float(precision), "recall": float(recall),
              "f1": float(f1), "macro_f1": float(f1_score(y, pred, average="macro")),
              "fpr": float(fp / max(1, fp + tn)), "fnr": float(fn / max(1, fn + tp)),
              "confusion_matrix": [[int(tn), int(fp)], [int(fn), int(tp)]]}
    if escalated is not None:
        result["escalated_count"] = int(escalated.sum()); result["escalated_fraction"] = float(escalated.mean())
    return result


def calibrated(p: np.ndarray) -> np.ndarray:
    c = json.loads((ROOT / "ml/v2/fast_calibration.json").read_text(encoding="utf-8"))
    logit = np.log(np.clip(p, 1e-8, 1 - 1e-8) / np.clip(1 - p, 1e-8, 1))
    return 1 / (1 + np.exp(-np.clip(logit * c["coefficient"] + c["intercept"], -50, 50)))


def context_flags(texts: list[str]) -> tuple[np.ndarray, np.ndarray, list[list[str]]]:
    from backend.app.brand_analyzer import analyze_brand_mismatch
    from backend.app.india_security import india_signals
    from backend.app.normalization import normalize_security, normalization_signals
    from backend.app.text_analyzer import analyze_text
    from backend.app.url_analyzer import analyze_url
    flags, strong, reasons = [], [], []
    for text in texts:
        normalized = normalize_security(text); finding = analyze_text(normalized.normalized_security_text)
        signals = [s for s in finding["signals"] if not s["id"].startswith("TXT_ML_")]
        signals += normalization_signals(normalized) + india_signals(normalized.normalized_security_text)
        for url in finding["urls"][:10]:
            try: signals += analyze_url(url)["signals"]
            except ValueError: pass
        signals += analyze_brand_mismatch(finding["clean_text"], finding["urls"])
        ids = {s["id"] for s in signals}; why = []
        if bool(ids & {"TXT_CREDENTIAL", "TXT_OTP", "INDIA_CREDENTIAL"}) and any(i.startswith(("URL_", "BRAND_")) for i in ids):
            why.append("credential_plus_url_or_brand")
        if any(i.startswith("NORM_") or i in {"TXT_ZERO_WIDTH", "TXT_MIXED_SCRIPT"} for i in ids):
            why.append("obfuscation")
        strong_evidence = sum(float(s["contribution"]) for s in signals) >= 40
        if strong_evidence:
            why.append("strong_deterministic_evidence")
        flags.append(bool(set(why) & {"credential_plus_url_or_brand", "obfuscation"})); strong.append(strong_evidence); reasons.append(why)
    return np.asarray(flags), np.asarray(strong), reasons


class Models:
    def __init__(self):
        self.vectorizer = joblib.load(ROOT / "ml/artifacts/text_vectorizer.joblib")
        self.fast = joblib.load(ROOT / "ml/artifacts/text_classifier.joblib")
        manifest = json.loads((ROOT / "ml/v2/deep_guard/manifest.json").read_text(encoding="utf-8"))
        self.temperature = manifest["temperature"]
        self.tokenizer = Tokenizer.from_file(str(ROOT / "ml/v2/deep_guard/tokenizer.json"))
        self.tokenizer.enable_truncation(max_length=128); self.tokenizer.enable_padding(length=128, pad_id=0, pad_token="[PAD]")
        opts = ort.SessionOptions(); opts.intra_op_num_threads = 4; opts.inter_op_num_threads = 1
        self.deep = ort.InferenceSession(str(ROOT / "ml/v2/deep_guard/model.onnx"), sess_options=opts, providers=["CPUExecutionProvider"])

    def predict(self, texts: list[str], escalate: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
        probabilities, elapsed = [], []
        for i, text in enumerate(texts):
            began = time.perf_counter()
            fast_raw = float(self.fast.predict_proba(self.vectorizer.transform([text]))[0, 1])
            value = float(calibrated(np.asarray([fast_raw]))[0])
            if escalate[i]:
                encoded = self.tokenizer.encode(text)
                inputs = {"input_ids": np.asarray([encoded.ids], np.int32), "attention_mask": np.asarray([encoded.attention_mask], np.int32)}
                logit = float(self.deep.run(None, inputs)[0].ravel()[0])
                value = 1 / (1 + math.exp(-max(-50, min(50, logit / self.temperature))))
            probabilities.append(value); elapsed.append((time.perf_counter() - began) * 1000)
        return np.asarray(probabilities), np.asarray(elapsed)


def route_mask(p: np.ndarray, context: np.ndarray, strong: np.ndarray, threshold: float) -> np.ndarray:
    entropy = -(p * np.log2(np.clip(p, 1e-8, 1)) + (1 - p) * np.log2(np.clip(1 - p, 1e-8, 1)))
    return (entropy >= threshold) | context | ((p < .25) & strong)


def main() -> None:
    val_x, val_y = read_tsv("validation")
    oof = np.load(ROOT / "ml/v2/fast_oof_predictions.npz")
    fast_val = calibrated(oof["probabilities"][-len(val_y):])
    deep_npz = np.load(ROOT / "ml/v2/experiments/bert_tiny/validation_predictions.npz")
    temperature = json.loads((ROOT / "ml/v2/experiments/bert_tiny/experiment.json").read_text(encoding="utf-8"))["temperature"]
    deep_val = 1 / (1 + np.exp(-np.clip(deep_npz["onnx_logits"] / temperature, -50, 50)))
    context_val, strong_val, _ = context_flags(val_x)
    deep_metrics = metric(val_y, deep_val)
    candidates = []
    for threshold in (.045, .08, .20, .40, .50, .60, .65, .70, .75, .80, .85, .90):
        mask = route_mask(fast_val, context_val, strong_val, threshold); combined = np.where(mask, deep_val, fast_val)
        report = metric(val_y, combined, mask); report["entropy_threshold"] = threshold
        report["quality_score"] = .45 * report["recall"] + .35 * report["macro_f1"] - .20 * report["fpr"] - .04 * report["escalated_fraction"]
        candidates.append(report)
    # v2.1's validation-minimal router failed the independent cross-domain ship gate.
    # v2.2 therefore reserves Fast-only decisions for calibrated p <= .005 or
    # p >= .995; entropy(.005) is ~.045. This is a fixed conservative confidence
    # boundary, not a threshold optimized on final-test labels.
    selected = next(c for c in candidates if c["entropy_threshold"] == .045)
    policy = {"schema_version": "1.0", "policy_version": "adaptive-v2.2", "entropy_threshold": selected["entropy_threshold"],
              "selection_source": "Post-v2.1 security ship-gate: fixed calibrated confidence bounds p<=.005 or p>=.995, audited on UCI validation OOF",
              "prior_policy_status": "adaptive-v2.1 rejected after cross-domain recall failed the ship gate; its report is preserved",
              "context_escalation": True,
              "selected_validation": selected, "deep_validation": deep_metrics, "fast_validation": metric(val_y, fast_val),
              "candidates": candidates, "test_used_for_selection": False,
              "validation_hash": hashlib.sha256((ROOT / "data/processed/uci_sms/validation.tsv").read_bytes()).hexdigest()}
    (ROOT / "ml/v2/router_policy.json").write_text(json.dumps(policy, indent=2), encoding="utf-8")

    models = Models()
    test_x, test_y = read_tsv("test")
    cross = json.loads((ROOT / "data/processed/cross_domain/mendeley_holdout.json").read_text(encoding="utf-8"))
    sets = {"uci_test": (test_x, test_y), "cross_domain": ([r["text"] for r in cross], np.asarray([r["label"] for r in cross]))}
    evaluation = {"policy": policy, "sets": {}}
    for name, (texts, labels) in sets.items():
        raw_fast = models.fast.predict_proba(models.vectorizer.transform(texts))[:, 1]; fast = calibrated(raw_fast)
        context, strong, reasons = context_flags(texts); mask = route_mask(fast, context, strong, selected["entropy_threshold"])
        adaptive, elapsed = models.predict(texts, mask)
        deep_all, _ = models.predict(texts, np.ones(len(texts), dtype=bool))
        evaluation["sets"][name] = {
            "fast_guard": metric(labels, fast), "deep_guard": metric(labels, deep_all), "adaptive": metric(labels, adaptive, mask),
            "adaptive_latency_ms": {"median": float(np.median(elapsed)), "mean": float(np.mean(elapsed)), "p95": float(np.percentile(elapsed, 95)), "repetitions": len(elapsed)},
            "context_escalations": int(context.sum()), "route_reason_counts": {r: sum(r in row for row in reasons) for r in ("credential_plus_url_or_brand", "obfuscation", "strong_deterministic_evidence")},
        }
    output = ROOT / "reports/v2/adaptive_routing_evaluation_v2.2.json"; output.write_text(json.dumps(evaluation, indent=2), encoding="utf-8")
    print(json.dumps(evaluation, indent=2))


if __name__ == "__main__":
    main()
