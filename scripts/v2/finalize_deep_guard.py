"""Freeze the validation-selected Deep Guard, then perform one-time final evaluations."""
from __future__ import annotations

import hashlib
import json
import math
import platform
from pathlib import Path
import shutil
import tempfile
import time

import joblib
import numpy as np
import onnx
import onnxruntime as ort
from sklearn.metrics import (accuracy_score, average_precision_score, brier_score_loss,
                             confusion_matrix, f1_score, precision_recall_fscore_support,
                             roc_auc_score)
from tokenizers import Tokenizer

ROOT = Path(__file__).resolve().parents[2]
EXPERIMENTS = ROOT / "ml/v2/experiments"
DEPLOY = ROOT / "ml/v2/deep_guard"
REPORTS = ROOT / "reports/v2"


def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def read_tsv(name: str) -> tuple[list[str], np.ndarray]:
    rows = (ROOT / f"data/processed/uci_sms/{name}.tsv").read_text(encoding="utf-8").splitlines()[1:]
    return [r.split("\t", 1)[1] for r in rows], np.asarray([int(r.split("\t", 1)[0]) for r in rows])


def measures(y: np.ndarray, p: np.ndarray) -> dict:
    pred = p >= .5
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    precision, recall, f1, _ = precision_recall_fscore_support(y, pred, average="binary", zero_division=0)
    return {
        "n": len(y), "accuracy": float(accuracy_score(y, pred)), "precision": float(precision),
        "recall": float(recall), "f1": float(f1), "macro_f1": float(f1_score(y, pred, average="macro")),
        "weighted_f1": float(f1_score(y, pred, average="weighted")),
        "fpr": float(fp / max(1, fp + tn)), "fnr": float(fn / max(1, fn + tp)),
        "roc_auc": float(roc_auc_score(y, p)), "pr_auc": float(average_precision_score(y, p)),
        "brier": float(brier_score_loss(y, p)), "confusion_matrix": [[int(tn), int(fp)], [int(fn), int(tp)]],
    }


def select() -> tuple[str, list[dict]]:
    records = []
    for directory in sorted(EXPERIMENTS.iterdir()):
        path = directory / "experiment.json"
        if not path.exists():
            continue
        item = json.loads(path.read_text(encoding="utf-8"))
        score = max(c["selection_score"] for c in item["curves"])
        records.append({"candidate": item["candidate"], "score": score, "bytes": item["onnx_bytes"],
                        "median_ms": item["cpu_inference_ms"]["median"], "recall": item["selection"]["recall"],
                        "macro_f1": item["selection"]["macro_f1"], "fpr": item["selection"]["fpr"]})
    best = max(r["score"] for r in records)
    eligible = [r for r in records if r["score"] >= best - .01]
    chosen = min(eligible, key=lambda r: (r["median_ms"], r["bytes"]))["candidate"]
    return chosen, records


class LocalModel:
    def __init__(self, path: Path, tokenizer: Tokenizer, temperature: float):
        opts = ort.SessionOptions(); opts.intra_op_num_threads = 4; opts.inter_op_num_threads = 1
        self.session = ort.InferenceSession(str(path), sess_options=opts, providers=["CPUExecutionProvider"])
        self.tokenizer, self.temperature = tokenizer, temperature

    def predict(self, texts: list[str]) -> tuple[np.ndarray, list[float], list[float]]:
        probabilities, prep, inference = [], [], []
        for text in texts:
            began = time.perf_counter(); encoded = self.tokenizer.encode(text); prep.append((time.perf_counter() - began) * 1000)
            data = {"input_ids": np.asarray([encoded.ids], np.int32), "attention_mask": np.asarray([encoded.attention_mask], np.int32)}
            began = time.perf_counter(); logit = float(self.session.run(None, data)[0].ravel()[0]); inference.append((time.perf_counter() - began) * 1000)
            probabilities.append(1 / (1 + math.exp(-max(-50, min(50, logit / self.temperature)))))
        return np.asarray(probabilities), prep, inference


def latency(prep: list[float], infer: list[float]) -> dict:
    total = np.asarray(prep) + np.asarray(infer)
    return {"median_ms": float(np.median(total)), "mean_ms": float(np.mean(total)), "p95_ms": float(np.percentile(total, 95)),
            "preprocessing_median_ms": float(np.median(prep)), "inference_median_ms": float(np.median(infer)), "repetitions": len(total)}


def fast_predictions(texts: list[str]) -> np.ndarray:
    vectorizer = joblib.load(ROOT / "ml/artifacts/text_vectorizer.joblib")
    classifier = joblib.load(ROOT / "ml/artifacts/text_classifier.joblib")
    raw = classifier.predict_proba(vectorizer.transform(texts))[:, 1]
    calibration = json.loads((ROOT / "ml/v2/fast_calibration.json").read_text(encoding="utf-8"))
    if not calibration["approved"]:
        return raw
    logit = np.log(np.clip(raw, 1e-8, 1 - 1e-8) / np.clip(1 - raw, 1e-8, 1))
    return 1 / (1 + np.exp(-np.clip(logit * calibration["coefficient"] + calibration["intercept"], -50, 50)))


def quantize(source: Path, destination: Path, tokenizer: Tokenizer, calibration_indices: list[int]) -> dict:
    from onnxruntime.quantization import CalibrationDataReader, CalibrationMethod, QuantFormat, QuantType, quantize_static
    val_x, _ = read_tsv("validation")
    class Reader(CalibrationDataReader):
        def __init__(self):
            self.data = []
            for i in calibration_indices[:256]:
                encoded = tokenizer.encode(val_x[i])
                self.data.append({"input_ids": np.asarray([encoded.ids], np.int32), "attention_mask": np.asarray([encoded.attention_mask], np.int32)})
            self.iterator = iter(self.data)
        def get_next(self):
            return next(self.iterator, None)
    # ORT 1.30 shape-inference temp paths corrupt the registered-symbol character on
    # this Windows workspace. Quantize the same bytes in an ASCII-safe temp folder.
    with tempfile.TemporaryDirectory(prefix="snapshield-qdq-") as temporary:
        temp_source = Path(temporary) / "model.onnx"
        temp_destination = Path(temporary) / "model.qdq.onnx"
        shutil.copy2(source, temp_source)
        quantize_static(str(temp_source), str(temp_destination), Reader(), quant_format=QuantFormat.QDQ,
                        activation_type=QuantType.QUInt8, weight_type=QuantType.QInt8,
                        per_channel=True, calibrate_method=CalibrationMethod.MinMax,
                        op_types_to_quantize=["MatMul", "Gemm"])
        shutil.copy2(temp_destination, destination)
    return {"format": "QDQ static INT8 MatMul/Gemm", "calibration_records": min(256, len(calibration_indices)),
            "calibration_source": "validation calibration partition", "sha256": sha(destination), "bytes": destination.stat().st_size}


def main() -> None:
    chosen, tournament = select()
    if chosen != "bert_tiny":
        raise RuntimeError(f"Selection policy unexpectedly chose {chosen}; review before reading test")
    experiment_dir = EXPERIMENTS / chosen
    experiment = json.loads((experiment_dir / "experiment.json").read_text(encoding="utf-8"))
    DEPLOY.mkdir(parents=True, exist_ok=True); REPORTS.mkdir(parents=True, exist_ok=True)
    shutil.copy2(experiment_dir / "model.onnx", DEPLOY / "model.onnx")
    shutil.copy2(experiment_dir / "tokenizer/tokenizer.json", DEPLOY / "tokenizer.json")
    tokenizer = Tokenizer.from_file(str(DEPLOY / "tokenizer.json")); tokenizer.enable_truncation(max_length=128); tokenizer.enable_padding(length=128, pad_id=0, pad_token="[PAD]")
    model = LocalModel(DEPLOY / "model.onnx", tokenizer, experiment["temperature"])

    test_x, test_y = read_tsv("test")
    cross_rows = json.loads((ROOT / "data/processed/cross_domain/mendeley_holdout.json").read_text(encoding="utf-8"))
    cross_x = [r["text"] for r in cross_rows]; cross_y = np.asarray([r["label"] for r in cross_rows])
    deep_test, test_prep, test_inf = model.predict(test_x)
    deep_cross, cross_prep, cross_inf = model.predict(cross_x)
    fast_test, fast_cross = fast_predictions(test_x), fast_predictions(cross_x)

    qdq_path = DEPLOY / "model.qdq.onnx"
    quant = quantize(DEPLOY / "model.onnx", qdq_path, tokenizer, experiment["calibration_indices"])
    qdq = LocalModel(qdq_path, tokenizer, experiment["temperature"])
    qdq_test, _, _ = qdq.predict(test_x); qdq_cross, _, _ = qdq.predict(cross_x)
    quant["test_class_agreement"] = float(np.mean((qdq_test >= .5) == (deep_test >= .5)))
    quant["test_max_probability_delta"] = float(np.max(np.abs(qdq_test - deep_test)))
    quant["cross_class_agreement"] = float(np.mean((qdq_cross >= .5) == (deep_cross >= .5)))
    quant["fp32_test"] = measures(test_y, deep_test); quant["qdq_test"] = measures(test_y, qdq_test)
    quant["fp32_cross_domain"] = measures(cross_y, deep_cross); quant["qdq_cross_domain"] = measures(cross_y, qdq_cross)
    quant["approved_for_qnn_validation"] = quant["test_class_agreement"] >= .995 and quant["qdq_test"]["recall"] >= quant["fp32_test"]["recall"] - .01

    result = {
        "schema_version": "1.0", "selection_frozen_before_test": True,
        "selection_policy": "Within 0.01 of best recall-weighted validation score, choose lowest measured CPU latency then size",
        "selected": chosen, "tournament": tournament, "test_read_count": 1,
        "uci_test_hash": sha(ROOT / "data/processed/uci_sms/test.tsv"),
        "cross_domain_hash": sha(ROOT / "data/processed/cross_domain/mendeley_holdout.json"),
        "fast_guard": {"uci_test": measures(test_y, fast_test), "cross_domain": measures(cross_y, fast_cross)},
        "deep_guard": {"uci_test": measures(test_y, deep_test), "cross_domain": measures(cross_y, deep_cross),
                       "uci_latency": latency(test_prep, test_inf), "cross_domain_latency": latency(cross_prep, cross_inf)},
        "quantization": quant,
        "environment": {"os": platform.platform(), "machine": platform.machine(), "onnxruntime": ort.__version__},
    }
    (REPORTS / "model_evaluation.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    graph = onnx.load(str(DEPLOY / "model.onnx"), load_external_data=False)
    manifest = {
        "schema_version": "1.0", "deployment_approved": True, "version": "deep-guard-bert-tiny-1.0",
        "model_name": "Deep Guard — BERT Tiny L2/H128", "candidate": chosen,
        "upstream": experiment["upstream"], "upstream_revision": experiment["revision"], "license": experiment["license"],
        "selection_policy": result["selection_policy"], "temperature": experiment["temperature"], "max_length": 128,
        "opset": experiment["opset"], "inputs": {i.name: [d.dim_value for d in i.type.tensor_type.shape.dim] for i in graph.graph.input},
        "outputs": [o.name for o in graph.graph.output], "operators": sorted({n.op_type for n in graph.graph.node}),
        "file_hashes": {p.name: sha(p) for p in (DEPLOY / "model.onnx", DEPLOY / "tokenizer.json", DEPLOY / "model.qdq.onnx")},
        "fp32_onnx_validation": experiment["onnx_validation"], "qnn_candidate": "model.qdq.onnx" if quant["approved_for_qnn_validation"] else None,
        "qnn_npu_verified": False, "snapdragon_hardware_validation": "PENDING — AI Hub credentials unavailable at freeze time",
    }
    (DEPLOY / "manifest.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
