# SnapShield AI v2 — project summary

SnapShield AI is a private, local-first multimodal cyber-defense application for Windows and Snapdragon PCs. It analyzes messages, URLs, screenshots, and QR codes with local ONNX inference, OCR, QR decoding, URL structure, brand/domain correlation, PII analysis, transparent security rules, an adaptive Fast/Deep router, and a Threat Evidence Graph. It returns bounded risk, evidence, and a practical action without visiting submitted destinations or requiring a cloud AI service.

The selected Deep Guard is BERT Tiny L2/H128. On the untouched 766-message UCI SMS test it reached 94.44% positive recall. On an independently sourced, strictly UCI-deduplicated 521-message 2022 Mendeley holdout it reached 98.04% recall. Adaptive v2.2 matched UCI Deep Guard recall with a 0.30% false-positive rate and 33.68% escalation. These are named SMS dataset results, not universal phishing accuracy.

The current development machine verifies ONNX Runtime and `CPUExecutionProvider`. Provider abstraction, a strict QNN route, QDQ candidate, exact-artifact validation, and Qualcomm AI Hub automation are implemented. QNN/Snapdragon NPU hardware validation is pending; no NPU latency, energy, or battery result is claimed.

The final package contains a smoke-tested unsigned AMD64 desktop build, eight real UI screenshots, two technical visuals, an eight-slide 16:9 PPTX/PDF deck, presenter and demo scripts, 100 judge Q&As, evaluation evidence, documentation, and SHA-256 integrity manifests.
