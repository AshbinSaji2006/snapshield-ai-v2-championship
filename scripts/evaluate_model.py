"""Re-evaluate the frozen final sklearn artifact on the untouched UCI test split."""
from __future__ import annotations

import json
from pathlib import Path

import joblib
import numpy as np
from sklearn.metrics import (
    accuracy_score,
    average_precision_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

ROOT = Path(__file__).resolve().parents[1]


def main() -> None:
    rows = (ROOT / "data/processed/uci_sms/test.tsv").read_text(encoding="utf-8").splitlines()[1:]
    labels, texts = zip(*[(int(row.split("\t", 1)[0]), row.split("\t", 1)[1]) for row in rows])
    y = np.asarray(labels)
    vectorizer = joblib.load(ROOT / "ml/artifacts/text_vectorizer.joblib")
    classifier = joblib.load(ROOT / "ml/artifacts/text_classifier.joblib")
    probability = classifier.predict_proba(vectorizer.transform(texts))[:, 1]
    predicted = (probability >= 0.5).astype(int)
    tn, fp, fn, tp = confusion_matrix(y, predicted, labels=[0, 1]).ravel()
    report = {
        "scope": "frozen final artifact on untouched UCI SMS test split",
        "samples": len(y),
        "accuracy": accuracy_score(y, predicted),
        "precision": precision_score(y, predicted),
        "recall": recall_score(y, predicted),
        "f1": f1_score(y, predicted),
        "macro_f1": f1_score(y, predicted, average="macro"),
        "weighted_f1": f1_score(y, predicted, average="weighted"),
        "false_positive_rate": fp / (fp + tn),
        "false_negative_rate": fn / (fn + tp),
        "roc_auc": roc_auc_score(y, probability),
        "pr_auc_average_precision": average_precision_score(y, probability),
        "confusion_matrix": [[int(tn), int(fp)], [int(fn), int(tp)]],
        "class_metrics": classification_report(y, predicted, target_names=["ham", "spam"], output_dict=True),
    }
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
