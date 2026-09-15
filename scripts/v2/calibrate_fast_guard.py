"""Fit Fast Guard calibration from OOF development predictions; never read the final test."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import brier_score_loss, confusion_matrix, f1_score
from sklearn.model_selection import StratifiedKFold, train_test_split

ROOT = Path(__file__).resolve().parents[2]
DATA = ROOT / "data/processed/uci_sms"
OUT = ROOT / "ml/v2/fast_calibration.json"


def read(name: str) -> tuple[list[str], np.ndarray]:
    rows = (DATA / f"{name}.tsv").read_text(encoding="utf-8").splitlines()[1:]
    return [r.split("\t", 1)[1] for r in rows], np.asarray([int(r.split("\t", 1)[0]) for r in rows])


def calibrator(x: np.ndarray, y: np.ndarray) -> LogisticRegression:
    model = LogisticRegression(C=1.0, random_state=42)
    logits = np.log(np.clip(x, 1e-8, 1 - 1e-8) / np.clip(1 - x, 1e-8, 1))
    model.fit(logits.reshape(-1, 1), y)
    return model


def apply(model: LogisticRegression, x: np.ndarray) -> np.ndarray:
    logit = np.log(np.clip(x, 1e-8, 1 - 1e-8) / np.clip(1 - x, 1e-8, 1))
    return model.predict_proba(logit.reshape(-1, 1))[:, 1]


def ece(y: np.ndarray, p: np.ndarray) -> float:
    value = 0.0
    for lower in np.arange(0, 1, .1):
        mask = (p >= lower) & (p < lower + .1 if lower < .9 else p <= 1)
        if mask.any():
            value += float(mask.mean() * abs(y[mask].mean() - p[mask].mean()))
    return value


def summary(y: np.ndarray, p: np.ndarray) -> dict:
    pred = p >= .5
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return {
        "n": len(y), "brier": float(brier_score_loss(y, p)), "ece_10_bins": ece(y, p),
        "macro_f1": float(f1_score(y, pred, average="macro")),
        "recall": float(tp / max(1, tp + fn)), "fpr": float(fp / max(1, fp + tn)),
        "confusion_matrix": [[int(tn), int(fp)], [int(fn), int(tp)]],
    }


def main() -> None:
    train_x, train_y = read("train"); val_x, val_y = read("validation")
    texts, labels = train_x + val_x, np.concatenate([train_y, val_y])
    folds = StratifiedKFold(5, shuffle=True, random_state=42)
    oof = np.zeros(len(labels), dtype=np.float64)
    for fit, held in folds.split(texts, labels):
        vectorizer = TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=15_000, sublinear_tf=True)
        classifier = LogisticRegression(C=7.0, max_iter=1000, class_weight={0: 1.0, 1: 2.0}, random_state=42)
        fit_text = [texts[i] for i in fit]; held_text = [texts[i] for i in held]
        classifier.fit(vectorizer.fit_transform(fit_text), labels[fit])
        oof[held] = classifier.predict_proba(vectorizer.transform(held_text))[:, 1]
    fit_idx, eval_idx = train_test_split(np.arange(len(labels)), test_size=.5, stratify=labels, random_state=42)
    audit_model = calibrator(oof[fit_idx], labels[fit_idx])
    raw, scaled = summary(labels[eval_idx], oof[eval_idx]), summary(labels[eval_idx], apply(audit_model, oof[eval_idx]))
    deploy_model = calibrator(oof, labels)
    approved = scaled["brier"] < raw["brier"] and scaled["macro_f1"] >= raw["macro_f1"] - .005
    payload = {
        "schema_version": "1.0", "approved": approved, "method": "Platt scaling on 5-fold OOF development predictions",
        "deployment_fit": "All train+validation OOF predictions", "evaluation": "Disjoint 50% of OOF predictions; calibrator fit on other 50%",
        "coefficient": float(deploy_model.coef_[0, 0]), "intercept": float(deploy_model.intercept_[0]),
        "audit_fit_coefficient": float(audit_model.coef_[0, 0]), "audit_fit_intercept": float(audit_model.intercept_[0]),
        "evaluation_raw": raw, "evaluation_calibrated": scaled, "test_read": False,
        "development_count": len(labels), "seed": 42,
        "oof_predictions_sha256": hashlib.sha256(oof.tobytes()).hexdigest(),
        "split_hashes": {n: hashlib.sha256((DATA / f"{n}.tsv").read_bytes()).hexdigest() for n in ("train", "validation")},
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    np.savez_compressed(ROOT / "ml/v2/fast_oof_predictions.npz", labels=labels, probabilities=oof)
    print(json.dumps(payload, indent=2))


if __name__ == "__main__":
    main()
