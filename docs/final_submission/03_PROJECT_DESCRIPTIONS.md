# Project descriptions

All performance statements below refer specifically to the deduplicated UCI SMS Spam Collection. Snapdragon NPU execution remains hardware-validation work.

## 50-word competition summary

SnapShield AI is a privacy-first cyber-defense copilot that analyzes suspicious messages, URLs, screenshots, QR codes, and sensitive data locally. It combines ONNX classification, OCR, QR decoding, URL forensics, PII redaction, and explainable risk fusion. CPU execution is verified today; its exact-gated QNN path is designed for Snapdragon validation on hardware.

## 100-word project listing

SnapShield AI is a private, on-device multimodal cyber-defense copilot for suspicious messages, URLs, screenshots, QR codes, and sensitive information. Its local pipeline combines a trained TF-IDF logistic classifier running through ONNX Runtime with RapidOCR, OpenCV QR decoding, structural URL forensics, social-engineering rules, brand-domain checks, PII redaction, and evidence-based risk fusion. The classifier achieved 98.17% held-out accuracy and 95.37% macro F1 on 766 deduplicated UCI SMS test messages. CPUExecutionProvider is verified today. A QDQ model, exact artifact-verification gate, and QNN HTP path are implemented for Snapdragon hardware validation, without claiming current NPU execution or performance in this audited competition build today.

## 150-word presentation description

SnapShield AI helps users inspect suspicious digital content without requiring that private material be sent to a cloud AI service. A user can provide a message, URL, screenshot, or QR image and receive a local risk score, specific evidence, redaction, and recommended action.

The system combines a lightweight TF-IDF logistic classifier with deterministic social-engineering indicators, Unicode-evasion checks, structural URL analysis, controlled brand-domain mismatch detection, local RapidOCR, OpenCV QR decoding, and PII detection. These independent findings enter a transparent risk-fusion policy; the classifier is supporting evidence rather than the final authority.

The model was trained using 5,105 deduplicated messages from the UCI SMS Spam Collection. On an untouched 766-message test split it achieved 98.17% accuracy, 86.67% spam recall, and 95.37% macro F1. FP32 ONNX predictions matched the reference classes for all test samples. CPU execution is verified; the QDQ/QNN path is implemented and awaits Snapdragon hardware validation on a compatible device.

## 250-word GitHub description

SnapShield AI is a privacy-first, multimodal cyber-defense copilot designed for Snapdragon PCs. It examines suspicious messages, URLs, screenshots, QR codes, and sensitive information without calling cloud AI or visiting submitted destinations.

The application uses specialized engines rather than relying on one black box. A word TF-IDF logistic-regression classifier provides learned message-risk evidence through ONNX Runtime. Deterministic engines detect social-engineering patterns, obfuscation, structural URL risks, controlled brand/domain mismatches, and PII. RapidOCR extracts screenshot text locally, while OpenCV decodes QR payloads. Their findings enter the same evidence model and a documented risk-fusion policy, producing a bounded score, severity, explanation, and practical recommendations.

The primary model uses the CC BY 4.0 UCI SMS Spam Collection. Deduplication occurred before a stratified seed-42 split: 5,574 original messages became 5,105 retained records, with 3,573 training, 766 validation, and 766 untouched test messages. The final test result was 98.17% accuracy, 97.50% spam precision, 86.67% spam recall, 91.76% spam F1, 95.37% macro F1, and a 0.30% false-positive rate. These metrics describe this SMS dataset, not universal phishing detection.

The 41,447-byte FP32 ONNX graph achieved 100% class agreement with the scikit-learn reference across all test samples. The verified development provider is CPUExecutionProvider. A QDQ candidate, dynamic provider abstraction, exact model-hash gate, and CPU-fallback-disabled QNN HTP validation path are implemented, but Snapdragon hardware was unavailable and no NPU performance claim is made.

The repository includes 77 passing backend tests, safe demonstration assets, presentation mode, sanitized SQLite incidents, separated CPU benchmarks, reproducible data/model scripts, and a smoke-tested unsigned AMD64 Windows build.

## 500-word portfolio narrative

SnapShield AI is a private, on-device multimodal cyber-defense copilot designed for suspicious messages, links, screenshots, QR codes, and sensitive information. The project begins with a simple observation: the content people want to inspect for scams is often the content they should be most careful about sharing. Messages may include banking context, personal conversations, email addresses, phone numbers, authentication instructions, or confidential business information. SnapShield keeps its core analysis on the PC instead of requiring a cloud AI request.

The product is intentionally not framed as a chatbot, spam filter, antivirus replacement, or universal phishing detector. It is a decision-support pipeline that combines specialized learned and deterministic components. Direct text, URLs, OCR output, and QR payloads enter a common orchestration layer. A word unigram/bigram TF-IDF logistic-regression model contributes a learned spam-risk probability. Separate engines identify social-engineering language, credential and payment requests, Unicode and spacing obfuscation, risky URL structure, and controlled brand/domain mismatch. A PII engine identifies and masks sensitive values. RapidOCR extracts screenshot text locally through ONNX Runtime, and OpenCV decodes QR content without navigating to it.

Each engine produces structured findings instead of an opaque verdict. Evidence includes a stable identifier, severity, contribution, description, and sanitized context. A deterministic fusion policy applies corroboration adjustments, bounds the score from zero to one hundred, assigns a severity, and generates an explanation plus recommended action. The ML model is one signal; a low classifier probability cannot overrule strong URL, credential, brand, QR, or obfuscation evidence. Optional local incident records contain hashes and sanitized metadata rather than source messages, images, full URLs, or secrets.

The final classifier was developed with the UCI SMS Spam Collection under CC BY 4.0. A reproducible pipeline verified the official archive checksum and removed 415 exact duplicates and 54 normalized near-duplicates before splitting. From 5,574 original messages, 5,105 were retained. A stratified seed-42 split produced 3,573 training, 766 validation, and 766 untouched test messages. Three lightweight candidates were compared. The selected model achieved 98.17% accuracy, 97.50% spam precision, 86.67% spam recall, 91.76% spam F1, 95.37% macro F1, a 0.30% false-positive rate, and a 13.33% false-negative rate on the test split. Those numbers are scoped to the named SMS dataset.

For deployment, the selected classifier was exported to a 41,447-byte FP32 ONNX graph using MatMul, Add, and Sigmoid. Across all 766 held-out samples, its classes matched the scikit-learn reference exactly, with a maximum probability difference of 9.24e-8. An 11,733-byte QDQ candidate achieved 99.739% class agreement with FP32.

The recorded development machine uses CPUExecutionProvider. Snapdragon NPU execution has not been verified. However, dynamic provider discovery, a QNN HTP path, CPU-fallback-disabled validation, exact artifact-hash gating, and automatic reporting are implemented. The engineering package also includes working OCR and QR analysis, 77 passing backend tests, frontend validation, separated CPU benchmarks, presentation mode, safe demos, documentation, and a smoke-tested unsigned AMD64 Windows build. The next milestones are named Snapdragon validation, native ARM64 packaging, broader modern datasets, multilingual support, and signed distribution. Until then, every hardware claim remains explicitly separated from measured, reproducible project evidence.
