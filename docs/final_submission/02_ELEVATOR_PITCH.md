# Elevator pitches and naming package

## Final naming package

- **Primary title:** SnapShield AI
- **Primary subtitle:** Private On-Device Multimodal Cyber Defense for Snapdragon PCs
- **Short subtitle:** Private Multimodal Security, On Device
- **Technical subtitle:** Local ONNX Cyber-Defense Pipeline with QNN-Ready Runtime
- **Primary tagline:** Your data never needs to leave your device to protect your device.
- **Marketing tagline:** Inspect threats locally. Understand the evidence. Act with confidence.
- **Ten-word descriptor:** Private multimodal threat analysis designed for local Snapdragon PC inference.

## Approximately 30 seconds

Security checks often begin with the most private things on a PC: messages, banking screenshots, links, QR codes, and personal information. SnapShield AI analyzes that content locally instead of requiring a cloud AI service. It combines a trained ONNX classifier with OCR, QR decoding, URL forensics, PII detection, and explainable risk fusion. The current build is CPU-verified, with an exact-gated QNN path designed for Snapdragon NPU validation. The result is risk, evidence, and action - not a chatbot guess.

## Approximately 60 seconds

When people receive a suspicious message, screenshot, URL, or QR code, checking it can mean sharing private conversations, account context, or authentication information with a remote service. SnapShield AI takes a different approach: its core security analysis stays on the PC.

It combines a lightweight message-risk classifier with local OCR, QR decoding, structural URL forensics, social-engineering indicators, controlled brand-domain checks, PII redaction, and transparent risk fusion. Instead of giving a black-box answer, it shows the score, the exact evidence, and the safest next action.

The classifier was trained on 5,105 deduplicated UCI SMS messages and achieved 98.17% held-out accuracy, 95.37% macro F1, and 86.67% positive recall on that dataset. The deployable model runs through ONNX Runtime with 100% class agreement against its scikit-learn reference across all 766 test samples.

Today the verified provider is CPUExecutionProvider. The QDQ model, provider abstraction, exact model-hash gate, and QNN HTP path are implemented for Snapdragon hardware validation. No NPU performance claim is being made. SnapShield's vision is continuous, privacy-first protection without mandatory cloud dependence.
