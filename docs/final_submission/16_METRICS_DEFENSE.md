# Metrics Defense

## The headline, correctly stated

“The selected text classifier achieved **98.1723% accuracy and 91.7647% F1 on a fixed 766-message test split of the retained UCI SMS Spam Collection corpus**.”

Never say “98.17% phishing accuracy.” The test corpus is SMS ham/spam, and the full SnapShield pipeline contains additional deterministic modules that were not measured by that headline.

## Test-set counts

| | Predicted ham | Predicted spam | Total |
|---|---:|---:|---:|
| Actual ham | 674 | 2 | 676 |
| Actual spam | 12 | 78 | 90 |
| Total | 686 | 80 | 766 |

From those counts:

- Accuracy: `(674 + 78) / 766 = 98.1723%`
- Precision: `78 / (78 + 2) = 97.5%`
- Recall: `78 / (78 + 12) = 86.6667%`
- F1: `91.7647%`
- False-positive rate: `2 / 676 = 0.2959%`
- False-negative rate: `12 / 90 = 13.3333%`
- ROC AUC: `0.992834`
- PR AUC: `0.972218`

## Why report more than accuracy

Spam is the minority class: the test split contains 90 spam and 676 ham messages. Accuracy alone can obscure missed attacks. Precision explains how often a spam prediction was correct; recall exposes the 12 missed spam samples; F1 balances those two concerns; false-positive and false-negative rates make the operational tradeoff explicit. PR AUC is especially informative when the positive class is uncommon.

## Leakage controls

The source had 5,574 rows. Deterministic preparation removed 415 exact duplicates and 54 normalized near-duplicates before splitting, leaving 5,105 rows. There were no normalized-text label conflicts. The retained data was split once with stratification and seed 42 into 3,573 train, 766 validation, and 766 test examples. Candidate selection used validation performance; the test set was reserved for final evaluation.

These controls reduce duplicate leakage and opportunistic test tuning. They do not eliminate domain limitations, annotation limitations, or temporal shift.

## Model selection

Three predeclared candidate pipelines were compared on the validation split. The winner was the word unigram/bigram TF-IDF logistic-regression model using `C=7.0` and class weights ham `1.0`, spam `2.0`. The selection criterion and artifacts are versioned, which makes the choice reproducible rather than post-hoc.

## ONNX equivalence

Deployment did not silently change the classifier. Native and FP32 ONNX outputs were compared across all 766 test examples. Class agreement was 100%; maximum absolute probability difference was `9.242706e-8`, and mean difference was `2.269248e-8`.

The QDQ candidate is treated separately: it was calibrated on 300 validation examples, used no test data for calibration, and achieved 99.7389% class agreement against FP32 with maximum probability difference 0.119397. Because that deviation is materially larger, FP32 remains the primary reported artifact.

## What the benchmark proves

The latency report measures the local pipeline on one AMD64 Windows development machine using `CPUExecutionProvider`. It supports statements about that environment only. It does not establish Snapdragon NPU latency, energy efficiency, thermals, or battery-life advantage. Browser rendering and incident persistence are excluded from the microbenchmark figures.

## What the adversarial suite proves

The 18/18 result means all 18 curated functional cases satisfied their expected invariants. It checks such behaviors as obfuscated indicators, safe parsing, redaction, and fusion consistency. Because it is a small curated suite rather than a sampled representative corpus, it must not be converted into a detection-accuracy percentage.

## Main threats to validity

1. **Dataset age and domain:** SMS spam does not represent the full modern phishing distribution across email, collaboration tools, QR lures, and multilingual content.
2. **Class imbalance:** only 90 positive examples appear in the test split, so a small number of errors moves recall materially.
3. **Duplicate policy:** deduplication improves leakage control but also changes comparability with papers that use the raw corpus.
4. **Threshold dependence:** precision and recall depend on the selected decision threshold and class weighting.
5. **Pipeline scope:** classifier metrics do not measure OCR, QR, URL, PII, or risk-fusion accuracy end to end.
6. **Hardware scope:** timings were measured on CPU in one development environment.

## Best judge answer

“The number I defend is 98.1723% accuracy on a specific, fixed, leakage-controlled SMS spam test split. The more security-relevant view is 97.5% precision and 86.67% recall, which exposes two false positives and twelve false negatives. It is strong validation of the compact text component, not proof that the full product catches 98% of phishing in the wild.”
