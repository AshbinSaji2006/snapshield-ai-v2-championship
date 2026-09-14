# SnapShield AI submission facts

Status: verified against repository artifacts on 2026-09-13. This file contains facts, boundaries, and approved claim language only.

## Identity

- Project: **SnapShield AI**
- Primary title: **SnapShield AI**
- Subtitle: **Private On-Device Multimodal Cyber Defense for Snapdragon PCs**
- Short subtitle: **Private Multimodal Security, On Device**
- Technical subtitle: **Local ONNX Cyber-Defense Pipeline with QNN-Ready Runtime**
- Primary tagline: **Your data never needs to leave your device to protect your device.**
- Marketing tagline: **Inspect threats locally. Understand the evidence. Act with confidence.**
- Ten-word descriptor: **Private multimodal threat analysis designed for local Snapdragon PC inference.**
- Category: privacy-first, multimodal cyber-defense decision-support application.
- It is not an antivirus replacement, cloud chatbot, URL-reputation service, or universal phishing detector.

## Verified product behavior

- Accepts messages, URLs, and PNG/JPEG/WEBP images.
- Image processing combines defensive decode, local OCR, local QR decoding, text/URL analysis, PII detection, risk fusion, explanation, and recommendations.
- Text engines detect learned spam patterns plus deterministic social-engineering and obfuscation signals.
- URL analysis is structural and never performs DNS, HTTP, redirect expansion, browser navigation, or payload execution.
- Controlled brand/domain mapping provides heuristic impersonation evidence.
- PII detection/redaction covers email, phone, Luhn-valid card numbers, IP addresses, JWTs, bearer/API tokens, password assignments, and private-key headers.
- SQLite stores SHA-256 source hashes and sanitized derived incident metadata, not raw messages, images, full URLs, or secrets.
- The production UI includes presentation mode, real demo inputs, exact runtime status, evidence, recommended actions, incidents, statistics, and deletion.
- Core analysis requires no cloud AI, telemetry, or network lookup after dependencies and models are installed.

## Dataset

- Name: UCI SMS Spam Collection.
- Publisher: UCI Machine Learning Repository.
- DOI: 10.24432/C5CC84.
- License: CC BY 4.0.
- Accessed: 2026-09-12.
- Official archive SHA-256: `1587ea43e58e82b14ff1f5425c88e17f8496bfcdb67a583dbff9eefaf9963ce3`.
- Original rows: 5,574.
- Retained after deduplication: 5,105.
- Exact duplicates removed before splitting: 415.
- Normalized near-duplicates removed before splitting: 54.
- Label conflicts removed: 0.
- Split: stratified 70/15/15, seed 42, after deduplication.
- Train: 3,573 (3,156 ham / 417 spam).
- Validation: 766 (676 ham / 90 spam).
- Untouched test: 766 (676 ham / 90 spam).
- The older 40-message synthetic corpus is retained only as historical prototype material and is not the primary evaluation.

## Model

- Name: **SnapShield UCI SMS Word TF-IDF Logistic Regression**.
- Version: 2.0.0.
- Features: 10,264 lowercased word unigram/bigram TF-IDF features.
- Classifier: logistic regression, C=7, class weights ham 1 / spam 2.
- Candidates evaluated: word TF-IDF/logistic; character TF-IDF/logistic; character TF-IDF/LinearSVC.
- Selection used validation recall, macro F1, false-positive rate, size, latency, ONNX compatibility, and local deployment suitability.
- Final training used train+validation after selection.
- A transformer was not evaluated; no performance claim against transformers is made.
- The classifier is one supporting signal, not the final security authority.

## Untouched UCI SMS test metrics

| Metric | Verified result |
|---|---:|
| Accuracy | 98.1723% |
| Spam precision | 97.5000% |
| Spam recall | 86.6667% |
| Spam F1 | 91.7647% |
| Macro F1 | 95.3684% |
| Weighted F1 | 98.1253% |
| False-positive rate | 0.2959% (2/676 ham) |
| False-negative rate | 13.3333% (12/90 spam) |
| ROC-AUC | 0.992834 |
| PR-AUC / average precision | 0.972218 |
| Confusion matrix | [[674, 2], [12, 78]] |

Approved wording: **The local message-risk classifier achieved 98.17% held-out accuracy on the deduplicated UCI SMS Spam Collection.**

Disallowed wording: **98.17% phishing detection accuracy.**

## ONNX

- Primary deployable path: ONNX Runtime.
- FP32 artifact: `text_classifier.onnx`, 41,447 bytes.
- Opset: 17; IR version: 10.
- Input: `features`, float32, dynamic batch by 10,264.
- Output: `probability`, float32, dynamic batch by 1.
- Operators: `MatMul`, `Add`, `Sigmoid`.
- Validation set for equivalence: all 766 untouched test samples.
- FP32/scikit-learn class agreement at 0.5: 100%.
- Maximum absolute probability difference: 9.242706e-8.
- Mean absolute probability difference: 2.269248e-8.
- QDQ candidate: `text_classifier.qdq.onnx`, 11,733 bytes.
- QDQ types: QUInt8 activations / QInt8 weights.
- QDQ calibration: first 300 validation records; no test records.
- QDQ/FP32 class agreement: 99.7389%.
- QDQ maximum absolute probability difference: 0.119397.
- QDQ is a target deployment candidate, not the current primary model.

## Runtime and Snapdragon

- Development machine: Intel64 Family 6 Model 186, AMD64, Windows 11 build 26200.
- ONNX Runtime: 1.30.0.
- Available providers in recorded validation: AzureExecutionProvider and CPUExecutionProvider.
- Current selected model provider: **CPUExecutionProvider**.
- QNN provider available: false.
- QNN SDK environment detected: false.
- Snapdragon validation report: `verified: false`.
- No Snapdragon NPU latency, speedup, power, or battery measurement exists.

**Verified on Snapdragon:** nothing yet.

**Implemented, hardware validation pending:** FP32 ONNX, QDQ candidate, dynamic provider discovery, QNN HTP path, CPU-fallback-disabled validation session, exact filename/SHA-256 verification gate, FP32 ONNX fallback, sklearn fallback, and automatic validation reporting.

**Planned/not implemented:** native ARM64 package, verified QNN graph assignment on Snapdragon, Qualcomm AI Hub compile/profile job, Snapdragon CPU/NPU comparison, code signing, and production installer/updater.

Approved wording: **Designed for Snapdragon NPU acceleration. QNN execution path implemented; hardware validation pending.**

Disallowed wording: **Running on Snapdragon NPU.**

## Recorded CPU benchmarks

Development machine only; medians:

- Cold ONNX model plus vectorizer load: 122.3451 ms (10 iterations).
- URL structural analysis: 0.0789 ms (500).
- TF-IDF preprocessing: 0.6348 ms (300).
- ONNX inference only: 0.0798 ms (500).
- PII detection/redaction: 0.1075 ms (500).
- QR decode: 34.4180 ms (100).
- Full text pipeline: 5.0894 ms (200).
- Full OCR + QR + security pipeline: 1,863.3500 ms (10).
- Browser rendering and incident persistence were excluded.
- These are not Snapdragon measurements.

## OCR, QR, testing, and security

- OCR: RapidOCR using ONNX Runtime; working locally.
- QR: OpenCV QRCodeDetector; working locally.
- Adversarial functional/calibration suite: 18/18 cases in expected bands. This is not model accuracy.
- Backend tests: 77 passed; latest verification 2026-09-13.
- Frontend lint: passed.
- Strict TypeScript: passed.
- Recorded production build: passed.
- npm audit: zero known vulnerabilities.
- pip check: no broken requirements.
- pip-audit: no known vulnerabilities after dependency upgrades.
- Security controls include loopback binding, trusted hosts, local-origin/CORS restrictions, CSP/security headers, parameterized SQL, React escaping, image byte/pixel/format validation, static-path containment, and sanitized persistence.
- Residual risks include local malware, native parser vulnerabilities, no global rate limiter, OCR/model/rule errors, and novel evasion.

## Desktop build

- Entry point: `release/SnapShieldAI/SnapShieldAI.exe`.
- Platform: Windows AMD64 one-folder PyInstaller build.
- Size: 372.28 MiB (390,359,552 bytes); 1,363 files.
- Executable SHA-256: `a3d07328f3f2a6d8b03a1bdb24ed8d800e59661330d32b941538bc74b2248036`.
- Authenticode status: NotSigned.
- Packaged evaluator flow: passed for dashboard, text, URL, OCR, QR, PII, incidents, statistics, runtime, benchmark, and production SPA assets.
- It is an unsigned competition build, not ARM64-native and not a signed installer.

## Final visual-capture facts

- Eight real packaged-application screenshots were captured at 1920 × 1080 on 2026-09-13.
- The captured dashboard reflects 19 sanitized local demo incidents, 65.2 average fused risk, and 12 high/critical demo records. These are accumulated synthetic demo-run analytics, not evaluation metrics.
- The captured bank-phish and multimodal examples each display a fused score of 100/critical. This is a bounded evidence score for those inert samples, not a calibrated probability or accuracy result.
- The captured Runtime page reports `CPUExecutionProvider`, hardware acceleration not detected, and Snapdragon NPU awaiting hardware validation.
- Its point-in-time interactive benchmark displays 25 iterations, 5.88 ms median, and 11.15 ms p95. That small live UI run does not replace the recorded 200-iteration 5.0894 ms benchmark above.
- The final presentation contains 8 slides in 16:9 and was exported through Microsoft PowerPoint to matching PPTX and PDF files.

## Known limitations

- Primary data is older English SMS spam, not a complete modern phishing corpus.
- Positive recall is 86.67%; 12 of 90 spam test messages were missed.
- Multilingual, email, business-email-compromise, and image-native attack coverage is limited.
- Screenshot results depend on OCR quality.
- Structural URL analysis has no live reputation context.
- Risk weights are transparent expert policy, not learned probabilities.
- Low risk is not a guarantee of safety.
- The real demo video, public repository publication, portal upload, presentation-laptop rehearsal, code signing, native ARM64 build, and Snapdragon hardware validation remain human or hardware tasks.
