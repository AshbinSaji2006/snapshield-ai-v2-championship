# SnapShield AI v2 — final claim audit

## Verdict

PASS for generated v2 submission-facing assets, subject to the external items explicitly marked pending. The audit distinguishes dataset metrics, development-CPU measurements, implemented deployment paths, and verified hardware execution.

## Approved evidence

| Claim | Status | Evidence |
|---|---|---|
| 5,105 deduplicated UCI messages | VERIFIED | UCI data manifest |
| Deep Guard UCI recall 94.44% | VERIFIED | 766-message untouched test; `model_evaluation.json` |
| Deep Guard external recall 98.04% | VERIFIED | 521-message Mendeley-derived holdout; `model_evaluation.json` |
| Adaptive UCI FPR 0.30% | VERIFIED | 2 FP / 676 negatives; `adaptive_routing_evaluation_v2.2.json` |
| 100 backend tests | VERIFIED | final pytest run |
| 20/20 functional checks | VERIFIED | `functional_evaluation.json`; not accuracy |
| 28.69 ms median full deep-routed pipeline | VERIFIED | final AMD64 CPU benchmark; not Snapdragon |
| FP32/QDQ class agreement 100% | VERIFIED | named UCI and external holdouts |
| Local ONNX inference through CPUExecutionProvider | VERIFIED | source tests, UI/runtime report, packaged smoke test |
| Core production analysis requires no cloud AI | VERIFIED | architecture, network-block tests, privacy review |
| QNN path/QDQ candidate/AI Hub automation | IMPLEMENTED BUT UNVERIFIED on hardware | source, model manifest, handoff |
| Snapdragon NPU execution/performance | PENDING | compatible hardware/authentication unavailable |
| Native Windows ARM64 package | PENDING | build instructions only |

## Wording audit

The v2 deck, README, scripts, portal answers, screenshots/captions, model card, and release documents were searched for `Snapdragon`, `NPU`, `QNN`, `ARM64`, `phishing`, `scam`, `accuracy`, `recall`, `multilingual`, `offline`, `privacy`, `performance`, `latency`, `power`, and known legacy metric values.

- No positive “NPU accelerated,” “runs on Snapdragon NPU,” “Snapdragon validated,” “45 TOPS used,” lower-power, battery-saving, or native-ARM64 claim is made.
- `CPUExecutionProvider` is the only verified application execution provider shown.
- QNN and Snapdragon NPU references state implemented path/candidate or hardware validation pending.
- Dataset metrics name their UCI or Mendeley-derived scope; no headline calls them universal phishing accuracy.
- Hinglish/Romanized Hindi results are called functional robustness, never multilingual accuracy.
- Risk score is described as an ordinal evidence index, not a calibrated probability.
- The 28.69 ms number is labeled as a current AMD64 development-CPU measurement, not Snapdragon performance.
- Cloud wording says cloud-dependent analysis *may* require remote processing; it does not claim all competitors upload everything.

## Presentation verification

- PPTX: 8 slides, 16:9.
- PDF: exported from the same PPTX through Microsoft PowerPoint.
- Slide proofs: 8 PNG files at 1920 × 1080.
- Visual review: hierarchy, clipping, screenshot crops, metric footnote, and CPU/QNN distinction checked.

## Required future re-audit

Rerun the claim audit after adding any public repository URL, demo-video captions, AI Hub results, ARM64 build, code signature, or portal-edited copy. Do not convert pending hardware statements into verified claims without exact-artifact and execution-unit evidence.
