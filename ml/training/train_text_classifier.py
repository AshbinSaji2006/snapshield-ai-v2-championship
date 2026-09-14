"""Compare lightweight classifiers, select on validation, and evaluate once on test."""
from __future__ import annotations

import json
import math
import sys
import time
from pathlib import Path

import joblib
import matplotlib.pyplot as plt
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (ConfusionMatrixDisplay, accuracy_score, average_precision_score,
                             classification_report, confusion_matrix, f1_score,
                             precision_recall_curve, precision_recall_fscore_support,
                             roc_auc_score, roc_curve)
from sklearn.svm import LinearSVC

ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = ROOT / "data" / "processed" / "uci_sms"
ARTIFACT_DIR = ROOT / "ml" / "artifacts"
RESULT_DIR = ROOT / "ml" / "evaluation" / "results"
SEED = 42


def read_split(name: str) -> tuple[list[str], np.ndarray]:
    rows = (DATA_DIR / f"{name}.tsv").read_text(encoding="utf-8").splitlines()[1:]
    labels, texts = zip(*[(int(row.split("\t", 1)[0]), row.split("\t", 1)[1]) for row in rows])
    return list(texts), np.asarray(labels, dtype=np.int64)


def metrics(y: np.ndarray, pred: np.ndarray, score: np.ndarray) -> dict:
    precision, recall, f1, _ = precision_recall_fscore_support(y, pred, average="binary", zero_division=0)
    tn, fp, fn, tp = confusion_matrix(y, pred, labels=[0, 1]).ravel()
    return {
        "accuracy": float(accuracy_score(y, pred)), "precision": float(precision), "recall": float(recall),
        "f1": float(f1), "macro_f1": float(f1_score(y, pred, average="macro")),
        "weighted_f1": float(f1_score(y, pred, average="weighted")),
        "false_positive_rate": float(fp / (fp + tn)), "false_negative_rate": float(fn / (fn + tp)),
        "roc_auc": float(roc_auc_score(y, score)), "pr_auc_average_precision": float(average_precision_score(y, score)),
        "confusion_matrix": [[int(tn), int(fp)], [int(fn), int(tp)]],
        "class_metrics": classification_report(y, pred, labels=[0, 1], target_names=["ham", "spam"], output_dict=True, zero_division=0),
    }


def build_candidates():
    return {
        "word_tfidf_logistic": (TfidfVectorizer(ngram_range=(1, 2), min_df=2, max_features=15_000, sublinear_tf=True), LogisticRegression(C=7.0, max_iter=1000, class_weight={0: 1.0, 1: 2.0}, random_state=SEED)),
        "char_tfidf_logistic": (TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2, max_features=20_000, sublinear_tf=True), LogisticRegression(C=5.0, max_iter=1000, class_weight={0: 1.0, 1: 1.7}, random_state=SEED)),
        "char_tfidf_linear_svm": (TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), min_df=2, max_features=20_000, sublinear_tf=True), LinearSVC(C=1.2, class_weight={0: 1.0, 1: 1.7}, random_state=SEED)),
    }


def main() -> None:
    train_x, train_y = read_split("train"); val_x, val_y = read_split("validation"); test_x, test_y = read_split("test")
    comparisons = {}
    trained = {}
    for name, (vectorizer, classifier) in build_candidates().items():
        started = time.perf_counter(); train_features = vectorizer.fit_transform(train_x); classifier.fit(train_features, train_y)
        validation_features = vectorizer.transform(val_x); pred = classifier.predict(validation_features)
        score = classifier.predict_proba(validation_features)[:, 1] if hasattr(classifier, "predict_proba") else classifier.decision_function(validation_features)
        report = metrics(val_y, pred, score); report["fit_time_seconds"] = time.perf_counter() - started; report["features"] = len(vectorizer.vocabulary_)
        report["selection_score"] = .45 * report["recall"] + .35 * report["macro_f1"] - .20 * report["false_positive_rate"]
        comparisons[name] = report; trained[name] = (vectorizer, classifier)
    best_score = max(item["selection_score"] for item in comparisons.values())
    deployable = [name for name in ("char_tfidf_logistic", "word_tfidf_logistic") if comparisons[name]["selection_score"] >= best_score - 0.02]
    selected = max(deployable, key=lambda name: comparisons[name]["selection_score"]) if deployable else max(comparisons, key=lambda name: comparisons[name]["selection_score"])
    vectorizer, classifier = build_candidates()[selected]
    combined_x = train_x + val_x; combined_y = np.concatenate([train_y, val_y])
    vectorizer.fit(combined_x); classifier.fit(vectorizer.transform(combined_x), combined_y)
    test_features = vectorizer.transform(test_x); pred = classifier.predict(test_features)
    score = classifier.predict_proba(test_features)[:, 1] if hasattr(classifier, "predict_proba") else 1 / (1 + np.exp(-classifier.decision_function(test_features)))
    test_report = metrics(test_y, pred, score)
    ARTIFACT_DIR.mkdir(parents=True, exist_ok=True); RESULT_DIR.mkdir(parents=True, exist_ok=True)
    joblib.dump(vectorizer, ARTIFACT_DIR / "text_vectorizer.joblib", compress=3)
    joblib.dump(classifier, ARTIFACT_DIR / "text_classifier.joblib", compress=3)
    manifest = json.loads((DATA_DIR / "dataset_manifest.json").read_text(encoding="utf-8"))
    model_name = "SnapShield UCI SMS Word TF-IDF Logistic Regression" if vectorizer.analyzer == "word" else "SnapShield UCI SMS Character TF-IDF Logistic Regression"
    metadata = {"model_name": model_name, "version": "2.0.0", "selected_candidate": selected, "selection_policy": "Recall-weighted validation score; deployable logistic model chosen when within 0.02 of best candidate", "dataset_sha256": manifest["sha256"], "features": len(vectorizer.vocabulary_), "preprocessing": {"analyzer": vectorizer.analyzer, "ngram_range": vectorizer.ngram_range, "lowercase": vectorizer.lowercase}, "splits": manifest["splits"], "test_metrics": test_report}
    (ARTIFACT_DIR / "model_metadata.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    (RESULT_DIR / "model_comparison.json").write_text(json.dumps(comparisons, indent=2), encoding="utf-8")
    (RESULT_DIR / "test_metrics.json").write_text(json.dumps(metadata, indent=2), encoding="utf-8")
    ConfusionMatrixDisplay.from_predictions(test_y, pred, display_labels=["Ham", "Spam"], cmap="Greens", colorbar=False); plt.title("Held-out UCI SMS test set"); plt.tight_layout(); plt.savefig(RESULT_DIR / "confusion_matrix.png", dpi=180); plt.close()
    fpr, tpr, _ = roc_curve(test_y, score); precision, recall, _ = precision_recall_curve(test_y, score)
    fig, axes = plt.subplots(1, 2, figsize=(10, 4)); axes[0].plot(fpr, tpr, color="#15966b"); axes[0].plot([0,1],[0,1],"--",color="#999"); axes[0].set(title=f"ROC AUC {test_report['roc_auc']:.3f}", xlabel="False positive rate", ylabel="True positive rate"); axes[1].plot(recall, precision, color="#15966b"); axes[1].set(title=f"PR AP {test_report['pr_auc_average_precision']:.3f}", xlabel="Recall", ylabel="Precision"); fig.tight_layout(); fig.savefig(RESULT_DIR / "roc_pr_curves.png", dpi=180); plt.close(fig)
    print(json.dumps(metadata, indent=2))


if __name__ == "__main__":
    main()
