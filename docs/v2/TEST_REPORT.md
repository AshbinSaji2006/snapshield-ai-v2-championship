# SnapShield AI v2 — final test report

Date: 2026-09-15 IST
Scope: v2 Championship repository only; frozen v1 was not modified.

## Final gates

| Gate | Result |
|---|---|
| Backend test suite | PASS — 100 tests |
| Curated functional robustness suite | PASS — 20/20 cases |
| Frontend lint | PASS — zero warnings |
| Strict TypeScript check | PASS |
| Frontend production build | PASS |
| Python dependency consistency | PASS — `pip check` found no broken requirements |
| Python advisory audit | PASS at audit time — no known vulnerabilities reported |
| npm production advisory audit | PASS at audit time — 0 vulnerabilities reported |
| PyInstaller one-folder build | PASS — 1,372 files, 432,986,557 bytes |
| Packaged executable smoke test | PASS — health and Deep-routed text analysis |
| Presentation export | PASS — 8 slides, 16:9 PPTX/PDF, 1920×1080 slide proofs |

## Packaged smoke evidence

The unsigned AMD64 `SnapShieldAI.exe` was launched with browser auto-open disabled. It bound to loopback only, returned version `2.0.0 Championship Candidate`, reported `CPUExecutionProvider`, and completed a synthetic inert phishing analysis with:

- critical risk, ordinal score 100;
- adaptive route `deep`;
- Deep Guard provider `CPUExecutionProvider`;
- URL, brand/domain, PII, rule, normalization, and Deep Guard evidence;
- a populated Threat Evidence Graph;
- no URL navigation.

The process was stopped after the smoke test. This is not a code-signing or target-laptop compatibility test.

## Final local benchmarks

Current AMD64 development PC only; not Snapdragon:

| Operation | Median | p95 | Repetitions |
|---|---:|---:|---:|
| Fast Guard | 1.16 ms | 2.02 ms | 100 |
| Deep Guard total | 10.42 ms | 22.36 ms | 50 |
| Full deep-routed text pipeline | 28.69 ms | 38.52 ms | 30 |
| URL engine | 0.15 ms | 1.90 ms | 100 |
| Evidence graph | 0.50 ms | 2.34 ms | 100 |
| QR decode | 198.87 ms | 263.47 ms | 10 |
| OCR | 3,304.17 ms | 3,721.89 ms | 5 |

OCR is the dominant local multimodal cost and remains a disclosed limitation. Complete raw output is `reports/v2/unified_benchmarks.json`.

## Model evaluation

The immutable machine-readable source is `reports/v2/model_evaluation.json` and routing evidence is `reports/v2/adaptive_routing_evaluation_v2.2.json`.

- Deep Guard UCI test: 98.56% accuracy, 94.44% positive recall, 0.89% FPR.
- Deep Guard independent external holdout: 98.85% accuracy, 98.04% positive recall, 0.63% FPR.
- Adaptive v2.2 UCI: 99.09% accuracy, 94.44% positive recall, 0.30% FPR, 33.68% escalated.
- QDQ candidate: 100% FP32 class agreement on both named holdouts.

These are named SMS dataset results, not universal phishing accuracy. Adaptive v2.2 was redesigned after v2.1’s external failure and is not presented as a pristine second independent-policy result.

## External checks still required

- Code signing and reputation checks on a signed build.
- Native Windows ARM64 build and presentation-laptop rehearsal.
- Strict QNN/Snapdragon NPU execution and numerical validation on compatible hardware.
- Real competition video recording and final portal preview.
