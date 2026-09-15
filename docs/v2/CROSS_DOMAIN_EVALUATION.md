# Cross-Domain Evaluation

The external evaluation uses the 2022 Mendeley SMS Phishing dataset (CC BY 4.0, DOI `10.17632/f45bkkt8pr.1`). From 5,971 source rows, strict exact/normalized and character-TF-IDF near-overlap filtering against all UCI splits plus internal deduplication retained 521 records: 317 ham, 87 spam and 117 smishing. The binary positive class combines source spam and smishing labels without silently modifying individual source labels.

Holdout SHA-256: `0b984c45b333e916fb1b6f61ac60b044f9d8dbb21270602a476e738422c7063f`.

| System | Accuracy | Precision | Recall | F1 | Macro F1 | FPR | FNR | Confusion matrix |
|---|---:|---:|---:|---:|---:|---:|---:|---|
| Fast Guard | 87.33% | 98.59% | 68.63% | 80.92% | 85.72% | 0.63% | 31.37% | TN 315, FP 2, FN 64, TP 140 |
| Deep Guard | 98.85% | 99.01% | 98.04% | 98.52% | 98.79% | 0.63% | 1.96% | TN 315, FP 2, FN 4, TP 200 |
| Adaptive v2.2 | 98.85% | 99.01% | 98.04% | 98.52% | 98.79% | 0.63% | 1.96% | TN 315, FP 2, FN 4, TP 200 |

Deep Guard demonstrates substantial incremental value under this domain shift. This set was never used to train or choose the neural candidate. The first adaptive router was evaluated on it and rejected; the v2.2 row is therefore a disclosed post-ship-gate diagnostic, not a second untouched benchmark.

The source CSV contains some publisher-distributed mojibake/replacement characters. The evaluation keeps those records rather than silently repairing semantic content, and the domain engine safely handles invalid IDNA.
