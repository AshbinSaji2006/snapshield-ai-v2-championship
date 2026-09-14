# Technical Summary

## System in one paragraph

SnapShield AI is a local FastAPI and React desktop-oriented application that accepts text, URL, or image input. A deterministic preprocessing boundary normalizes submitted content; image inputs are decoded locally by RapidOCR and OpenCV QR detection. A compact ONNX text classifier, social-engineering detector, URL forensic analyzer, PII/secret detector, and brand/domain consistency engine generate independent evidence. Risk fusion turns that evidence into a bounded score, severity, explanation, and recommended action. The application reports the selected ONNX Runtime execution provider and persists only sanitized incident metadata.

## Request flow

1. The React interface sends the explicitly submitted content to the loopback FastAPI service.
2. Input guards enforce accepted types and limits: text up to 50,000 characters, URL up to 4,096 characters, and PNG/JPEG/WEBP images up to 10 MB.
3. Text is normalized; URLs are extracted and defanged forms can be recognized. For images, local OCR extracts visible text and QR decoding extracts payloads.
4. The text featurizer produces a 10,264-element sparse TF-IDF representation using word unigrams and bigrams.
5. The ONNX classifier returns a spam-like score. Parallel deterministic modules generate concrete evidence from wording, URL structure, privacy patterns, and brand/domain mismatches.
6. Risk fusion applies transparent evidence weights and caps to produce the user-facing score. The score is an operational risk score, not a probability calibration claim.
7. The response includes category, severity, indicators with contributions, explanation, recommended actions, redacted text where relevant, runtime provider, and processing time.
8. The incident store retains a SHA-256 input hash and sanitized decision metadata. Raw source, images, full URLs, secrets, and extracted PII are not persisted.

## Why this model

The primary model is `snapshield_tfidf_logreg_word12_v1`, a logistic-regression classifier trained on TF-IDF word unigrams and bigrams. It was selected from three predeclared candidates using the fixed validation split, then evaluated once on the untouched test split.

This model is intentionally lightweight. Phishing defense benefits from predictable latency, a small deployable artifact, reproducible training, and the ability to explain which independent evidence changed the decision. A general-purpose transformer could improve semantic coverage in some cases, but it would increase package size, memory use, accelerator constraints, and explanation complexity. SnapShield instead assigns concrete structure—URLs, QR payloads, PII, urgency, and brand mismatches—to deterministic security engines, leaving the model to capture message-language patterns.

The production ONNX file is 41,447 bytes because the vocabulary and feature mapping live in the application artifact set while the graph itself contains the learned linear layer: `MatMul → Add → Sigmoid`. This is not presented as a universal phishing model; it is one verified component in a defense-in-depth system.

## Dataset and training contract

- Source: UCI SMS Spam Collection, DOI `10.24432/C5CC84`, CC BY 4.0.
- Downloaded source: yes; its SHA-256 and access date are recorded.
- Original rows: 5,574; retained after deterministic cleaning: 5,105.
- Removal: 415 exact duplicates and 54 normalized near-duplicates; no conflicting normalized labels.
- Fixed stratified 70/15/15 split with seed 42: 3,573 train, 766 validation, 766 test.
- Test isolation: the test split was not used for model selection.

## Verified primary-model results

On the fixed 766-message test split, the primary model achieved 98.1723% accuracy, 97.5% precision, 86.6667% recall, 91.7647% F1, 0.2959% false-positive rate, and 13.3333% false-negative rate. The confusion matrix is `[[674, 2], [12, 78]]`, ordered as true label rows and predicted label columns for ham/spam. ROC AUC was 0.992834 and PR AUC was 0.972218.

These are results on a cleaned SMS spam dataset, not a measured real-world phishing detection rate. The 18-case adversarial suite checks functional invariants and robustness behaviors; it is not a statistical benchmark.

## ONNX validation

The production FP32 model uses ONNX opset 17 and IR version 10. It accepts `features` with shape `[batch, 10264]` and produces `[batch, 1]`. Across all 766 test examples, native and ONNX classifications agreed on 100% of cases; maximum probability difference was `9.242706e-8` and mean difference was `2.269248e-8`.

A 11,733-byte QDQ quantized candidate was calibrated on 300 validation examples, never on the test split. It retained 99.7389% class agreement against FP32 on the test set, but its maximum probability difference was 0.119397. It is NPU-prepared and is not the primary reported model.

## Runtime and Snapdragon path

At startup, the runtime inspects available ONNX Runtime providers. CPU is the dependable fallback. A QNN path is configured for compatible Snapdragon hardware, including an NPU-oriented QDQ artifact and strict verification that rejects silent CPU fallback. The application records artifact hashes and exposes provider status in the UI and machine-readable reports.

The audited development machine is AMD64 Windows build 26200 with ONNX Runtime 1.30.0. Available providers were Azure and CPU, so `CPUExecutionProvider` was selected. No Snapdragon NPU execution, QNN performance, power, or thermals have been measured. ARM64 packaging, a real QNN/HTP run, AI Hub job evidence, and device benchmarking remain future validation work.

## Measured local performance

CPU microbenchmark medians on the audited development machine include 0.0789 ms for URL analysis, 0.6348 ms for TF-IDF featurization, 0.0798 ms for ONNX inference, 0.1075 ms for PII analysis, 34.418 ms for QR decode, 5.0894 ms for the full text pipeline, and 1,863.35 ms for the full multimodal pipeline. Cold start median was 122.3451 ms. These timings exclude browser rendering and incident persistence and must not be presented as Snapdragon results.

## Security and privacy properties

- No cloud AI integration is enabled.
- Suspicious URLs are parsed, not navigated.
- MIME/type and size guards constrain uploaded images.
- PII/secret patterns are redacted by default.
- Persistent incident records are sanitized and deletable.
- Runtime reports distinguish verified providers from intended providers.
- Artifact hashes make the evaluated and packaged build traceable.

## Verification surface

The verified project state includes 77 passing backend tests, passing frontend lint and strict TypeScript checks, a successful production build, passing Python and npm dependency audits, ONNX equivalence artifacts, deterministic data manifests, benchmark reports, and a packaged AMD64 build whose executable hash is recorded in [01_PROJECT_FACTS.md](01_PROJECT_FACTS.md).
