# Adversarial and India-Focused Functional Evaluation

Twenty safe, deterministic cases exercise the real pipeline. Coverage includes legitimate personal/urgent/marketing messages, official and mismatched brand domains, `hxxp`, `[.]`, spaced URLs, zero-width insertion, Punycode, Cyrillic homoglyph normalization, a shortener, no-URL lure, credential/payment requests, and India-relevant KYC, electricity, UPI refund, digital-arrest, recruitment and customs-parcel patterns.

Result: **20/20 functional checks passed** after two genuine rule defects were corrected: digital-arrest secrecy language was incorrectly treated as benign negation, and the parcel/customs rule assumed only one word order. The initial 17/20 run was not erased from the work narrative; the final machine-readable report is `reports/v2/functional_evaluation.json`.

This is a curated functional robustness suite, not classifier accuracy, Hindi accuracy, or a population estimate. The cases are original safe test fixtures and use `.example` or documentation-only IP destinations.
