# Datasets

## Primary model dataset

| Field | Value |
|---|---|
| Name | SMS Spam Collection |
| Publisher | UCI Machine Learning Repository |
| DOI | 10.24432/C5CC84 |
| Source | <https://archive.ics.uci.edu/dataset/228/sms+spam+collection> |
| Download | <https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip> |
| License | Creative Commons Attribution 4.0 (CC BY 4.0) |
| Accessed | 2026-09-12 |
| Archive SHA-256 | `1587ea43e58e82b14ff1f5425c88e17f8496bfcdb67a583dbff9eefaf9963ce3` |
| Original rows | 5,574 |
| Retained | 5,105 |
| Labels | `ham`, `spam` |

The reproducible pipeline is `ml/data/prepare_uci_sms.py`. It downloads only the official UCI archive, verifies the pinned checksum, decodes the source, maps labels, and removes duplicates **before** splitting. It removed 415 exact duplicates and 54 normalized near-duplicates; no label conflicts remained. Normalized comparison case-folds text, replaces URLs/numbers with markers, and collapses non-word spacing to reduce template leakage.

Seed 42 stratified split:

| Split | Rows | Ham | Spam | Use |
|---|---:|---:|---:|---|
| Train | 3,573 | 3,156 | 417 | Candidate fitting |
| Validation | 766 | 676 | 90 | Selection and threshold/configuration decisions |
| Test | 766 | 676 | 90 | One final untouched evaluation |

The final model is retrained on train+validation only after selection. The dataset manifest and derived TSVs are in `data/processed/uci_sms`; attribution is in `data/raw/ATTRIBUTION.md`.

## Curated functional/adversarial corpus

`ml/evaluation/adversarial_cases.json` contains 18 project-authored safe cases: 6 benign and 12 suspicious. It tests legitimate security notices, brand mismatch, defanged URLs, IP URLs, punycode, `@` URLs, nested subdomains, zero-width characters, mixed scripts, spaced credentials, and gift-card authority scams.

All 18 currently land in their expected risk bands. At a moderate threshold the functional confusion matrix is `[[6,0],[0,12]]`. This is explicitly a small deterministic regression/calibration suite, **not model accuracy or a real-world FPR/FNR claim**.

`ml/data/security_messages.tsv` is the original 40-message synthetic prototype corpus. It remains only for historical/reproducibility context and is not used for the primary model or performance claim.

## Known data limitations

UCI SMS messages are older, English-language, short-form, and spam-focused. They do not represent all current enterprise phishing, screenshots, multilingual attacks, or business-email compromise. The test metrics establish performance on this named corpus only.
