# Data and evaluation protocol — frozen before v2 training

## Sources

- UCI SMS Spam Collection, Tiago Almeida / José María Gómez Hidalgo, [DOI 10.24432/C5CC84](https://doi.org/10.24432/C5CC84), CC BY 4.0. Preserve all original processed split bytes and v1 classifier artifacts.
- Sandhya Mishra / Devpriya Soni, [SMS Phishing Dataset V1](https://data.mendeley.com/datasets/f45bkkt8pr/1), DOI 10.17632/f45bkkt8pr.1, published 2022-06-20, CC BY 4.0. Original archive `Dataset_5971.zip`, 244,698 bytes; publisher SHA-256 `9bbf3188fdad81495d8e82825648b9b63b53fc86841a3d26c02629990b233cc3`. 5,971 source records reported; preserve actual observed counts separately. Attribution/license checked 2026-09-15. Use only as cross-dataset evaluation, not training or threshold tuning.
- Original SnapShield examples: synthetic functional regression only. English, Hindi, Romanized Hindi, Hinglish, benign counterexamples, reserved domains. No real-world accuracy or Hindi accuracy claim.

## Leakage and selection

Train neural candidates on the 3,573 UCI training messages only. Split original 766 validation messages deterministically into selection and calibration halves, stratified seed 42. Choose model/checkpoint using selection half, fit calibration using calibration half. Final test remains 766 fixed messages and is evaluated after selection; never optimize thresholds against it.

For frozen Fast Guard calibration, use five-fold out-of-fold predictions across its training population (3,573 + 766). Fit probability calibration to these predictions. Report calibration evaluation on held-out folds/partitions, not the rows used to fit a calibrator. Fast Guard's existing threshold and weights remain available independently.

Cross-dataset evaluation excludes exact and normalized matches against ALL UCI splits, then excludes close character n-gram matches at cosine similarity >= 0.90. Deduplicate internally before evaluation. Quarantine cross-label conflicts rather than guessing labels. Record all exclusions by reason and hashes; these are leakage controls fixed before evaluating model errors, not removal of difficult samples. Keep original spam/smishing labels as subgroups; a combined positive class is called spam-or-smishing, not universally malicious.

## Predeclared tournament gate

Candidates: Google BERT Tiny (2 layers, 128 hidden); Sentence Transformers MiniLM L6 (6 layers, 384 hidden); DistilBERT (6 layers, 768 hidden) if memory/runtime permits. All require an explicit reusable model license, pinned upstream revision, safe tensor weights and local ONNX export. Google BERT Mini / Huawei TinyBERT with pickle-only upstream weights are not preferred in this environment.

Train seed 42, up to 4 epochs, AdamW, sequence length 128. Select checkpoint by `0.45*recall + 0.35*macro_f1 - 0.20*FPR`, with FPR <= 0.02 on the selection partition. If none qualify, retain Fast Guard as production default. Among qualifying candidates within 0.015 of the best selection score, prefer lower CPU latency/model size. Deployment gate also requires class equivalence >= 99.9% and no unsupported silent provider claims.

No cross-domain result will be used to select a different model after inspection. No modern 2026 empirical performance claim is justified by the 2022 dataset. Smishtank's article and unrelated mirrors do not establish a reusable corpus license; exclude until verified. The 2025 LLM-balanced Mendeley set is synthetic, so do not present it as modern real-world evidence.
