# Model card - SnapShield text classifier v2.0.0

## Intended use

The model supplies one local supporting signal for English SMS spam/phishing screening. It is not antivirus, a URL-reputation service, proof of malicious intent, or the sole source of the application verdict.

## Model and selection

- Selected: word TF-IDF unigrams/bigrams plus logistic regression (`C=7`, class weights ham 1 / spam 2).
- Input: UTF-8 text transformed outside ONNX to 10,264 dense `float32` TF-IDF features.
- Output: spam probability in `[0,1]`; operational threshold 0.5.
- Selection: recall-weighted validation score including macro F1 and FPR, with deployment/ONNX suitability. A logistic model was preferred when within 0.02 of the best validation score.
- Runtime: ONNX Runtime primary; serialized scikit-learn fallback.
- Version: `2.0.0`.

Validation candidates on the 766-row validation split:

| Candidate | Precision | Recall | Macro F1 | FPR | FNR | PR-AUC |
|---|---:|---:|---:|---:|---:|---:|
| Word TF-IDF + logistic | 1.0000 | 0.9111 | 0.9738 | 0.0000 | 0.0889 | 0.9728 |
| Char TF-IDF + logistic | 0.9873 | 0.8667 | 0.9568 | 0.0015 | 0.1333 | 0.9795 |
| Char TF-IDF + LinearSVC | 0.9878 | 0.9000 | 0.9673 | 0.0015 | 0.1000 | 0.9789 |

The selected configuration was retrained on train+validation. A transformer was not evaluated: no licensed task-specific checkpoint was already available offline, training/fine-tuning a generic transformer would materially enlarge the dependency and deployment footprint, and it was not justified for this 5,105-row corpus. This is a documented limitation, not an inference that a transformer would perform worse.

## Data

UCI SMS Spam Collection, DOI [`10.24432/C5CC84`](https://doi.org/10.24432/C5CC84), licensed under Creative Commons Attribution 4.0 (CC BY 4.0). The source contains 5,574 original rows and 5,105 retained after 415 exact and 54 normalized near-duplicate removals. Splits were created only after deduplication: train 3,573, validation 766, test 766. See [DATASETS.md](DATASETS.md).

## Untouched test result

The test set was evaluated once after model selection and final retraining.

| Metric | Value |
|---|---:|
| Accuracy | 0.981723 |
| Spam precision | 0.975000 |
| Spam recall | 0.866667 |
| Spam F1 | 0.917647 |
| Macro F1 | 0.953684 |
| Weighted F1 | 0.981253 |
| FPR | 0.002959 |
| FNR | 0.133333 |
| ROC-AUC | 0.992834 |
| PR-AUC / average precision | 0.972218 |

Confusion matrix, rows actual and columns predicted `[ham, spam]`: `[[674, 2], [12, 78]]`.

- Ham (n=676): precision 0.9825, recall 0.9970, F1 0.9897.
- Spam (n=90): precision 0.9750, recall 0.8667, F1 0.9176.

Artifacts: `ml/evaluation/results/test_metrics.json`, `confusion_matrix.png`, and `roc_pr_curves.png`.

## ONNX validation

The FP32 graph uses opset 17, IR 10, and only `MatMul`, `Add`, and `Sigmoid`. It is 41,447 bytes. Across all 766 held-out samples, maximum probability difference from scikit-learn was `9.24e-8`, mean difference `2.27e-8`, and class agreement at 0.5 was 100%.

The 11,733-byte QDQ candidate uses QUInt8 activations/QInt8 weights calibrated on 300 validation records, never test data. Versus FP32 it achieved 99.739% class agreement; maximum probability difference was 0.1194. It remains a deployment candidate until full no-CPU-fallback QNN/HTP validation on Snapdragon hardware.

## Limitations and risk controls

The dataset is English SMS from an older collection and is strongly imbalanced. The spam false-negative rate is 13.33%, so model confidence cannot be treated as a safety guarantee. Modern QR phishing, Unicode attacks, branded credential harvesting, multilingual content, and business-email compromise are incompletely represented. SnapShield mitigates this with independent deterministic signals, explicit evidence, cautious wording, adversarial functional tests, and human-verification recommendations.
