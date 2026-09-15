# Adaptive Fast/Deep Routing

Fast Guard is the always-available TF-IDF logistic first pass. Deep Guard is the selected BERT Tiny ONNX model. The router uses calibrated Fast probability entropy plus deterministic context: credential solicitation with URL/brand evidence, normalized obfuscation, QR correlation, low OCR confidence, and disagreement with strong rules. Every response exposes the decision class and reasons.

Decision classes are `FAST_ONLY_SAFE`, `FAST_ONLY_HIGH_CONFIDENCE`, `ESCALATE_UNCERTAIN`, `ESCALATE_HIGH_RISK_CONTEXT`, and `ESCALATE_MULTIMODAL`.

## Rejected v2.1 policy

The initial validation-minimal threshold escalated about 7–8% of test inputs. It improved cross-domain recall from Fast Guard's 68.63% to 76.96%, but remained far below Deep Guard's 98.04%. It failed the ship gate and is preserved in `reports/v2/adaptive_routing_evaluation.json` as **REJECTED**.

## Shipping v2.2 policy

The shipping policy reserves Fast-only decisions for calibrated extreme-confidence bounds (`p <= 0.005` or `p >= 0.995`); entropy threshold 0.045 implements that boundary, while contextual triggers can still escalate. The policy file records that this conservative redesign followed the v2.1 cross-domain failure. It is not presented as a pristine independent second evaluation.

| Set | Fast recall / FPR | Deep recall / FPR | Adaptive recall / FPR | Deep escalations |
|---|---:|---:|---:|---:|
| UCI final test, 766 | 88.89% / 0.59% | 94.44% / 0.89% | 94.44% / 0.30% | 33.68% |
| Mendeley external, 521 | 68.63% / 0.63% | 98.04% / 0.63% | 98.04% / 0.63% | 51.25% |

The final router matched Deep Guard recall on both evaluated sets while avoiding Deep inference on 66.32% and 48.75% of inputs respectively. Latency claims come only from the separate unified benchmark because evaluation-loop timings include instrumentation overhead.
