# Deep Guard Model Tournament

## Protocol

Three Apache-2.0 compact encoders were fine-tuned on the 3,573-message UCI training split. The 766-message validation split was divided deterministically into 383 selection and 383 calibration records. The final test and Mendeley holdout were not read during selection. Candidate score was `0.45 recall + 0.35 macro F1 - 0.20 FPR`, with FPR above 2% rejected. Temperature scaling used only the calibration partition.

| Candidate | Selection recall | Macro F1 | FPR | Score | ONNX size | CPU median | ONNX agreement |
|---|---:|---:|---:|---:|---:|---:|---:|
| BERT Tiny L2/H128 | 91.11% | 97.38% | 0.00% | 0.7508 | 17.52 MB | 3.25 ms | 100% / 766 |
| MiniLM L6 | 93.33% | 96.22% | 0.89% | 0.7550 | 90.34 MB | 48.47 ms | 100% / 766 |
| DistilBERT | 93.33% | 96.82% | 0.59% | 0.7577 | 265.52 MB | 153.22 ms | 100% / 766 |

## Selection

The rule fixed before test access was: among models within 0.01 of the best validation score, choose the lowest measured CPU latency, then size. All three qualified. **BERT Tiny** was selected: its score was only 0.0069 behind DistilBERT, while it was about 15× faster in the tournament measurement and 15× smaller. This is an edge-security Pareto choice, not a claim that it is universally the most accurate transformer.

## One-time evaluation

On the untouched 766-message UCI test, Deep Guard reached 98.56% accuracy, 94.44% recall, 93.41% precision, 93.92% F1, 96.55% macro F1, 0.89% FPR and 5.56% FNR. On the independently deduplicated 521-message Mendeley set it reached 98.85% accuracy, 98.04% recall, 99.01% precision, 98.52% F1, 98.79% macro F1, 0.63% FPR and 1.96% FNR.

These are SMS message-classification results on named datasets. They are not universal phishing-detection accuracy.

Source evidence: `ml/v2/experiments/*/experiment.json`, `reports/v2/model_evaluation.json`, and `ml/v2/deep_guard/manifest.json`.
