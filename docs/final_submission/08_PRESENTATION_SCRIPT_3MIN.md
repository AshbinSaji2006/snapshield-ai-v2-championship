# Presentation script - three minutes

## 0:00-0:20 - Hero

"SnapShield AI is a private, on-device multimodal cyber-defense copilot designed for Snapdragon PCs. It analyzes suspicious messages, links, screenshots, QR codes, and sensitive information, then returns risk, evidence, and a practical action."

## 0:20-0:45 - Problem

"Security inputs are unusually private. A suspicious message may include banking context, authentication instructions, or confidential conversations. Screenshots and QR codes also hide important evidence. Requiring remote analysis adds a trust and connectivity boundary before the user even knows whether the content is safe."

## 0:45-1:15 - Solution and architecture

"SnapShield keeps core analysis local. RapidOCR extracts screenshot text; OpenCV decodes QR payloads; an ONNX classifier supplies learned message-risk evidence; and deterministic engines inspect social engineering, Unicode evasion, URL structure, brand mismatch, and PII. A transparent fusion policy turns these findings into a bounded score, explanation, and recommendation. URLs are never opened, and raw source content is not stored in incidents."

## 1:15-1:55 - Evidence

"The classifier uses the CC BY 4.0 UCI SMS Spam Collection. Deduplication happened before splitting: 5,105 messages were retained, with an untouched 766-message test set. On that dataset, the model achieved 98.17 percent accuracy, 95.37 percent macro F1, and 86.67 percent spam recall. The false-positive rate was 0.30 percent. Its 41-kilobyte ONNX export matched the reference class on every test sample. The backend has 77 passing tests, and the full text pipeline measured a 5.09-millisecond median on the development CPU."

## 1:55-2:30 - Snapdragon

"The current verified provider is CPUExecutionProvider on Intel AMD64 - not a Snapdragon NPU. The Snapdragon-ready work is concrete: an ONNX model, QDQ candidate, provider abstraction, QNN HTP path, CPU-fallback-disabled validation, exact model-hash gating, and automatic reporting. Hardware was unavailable, so no NPU speed or battery claim is made."

## 2:30-3:00 - Impact and close

"This architecture makes the strongest demo a screenshot: OCR text, a QR destination, URLs, PII, and social-engineering evidence are analyzed together without leaving the PC. SnapShield can complement existing security tools with understandable local triage for students, families, professionals, and organizations. Private AI. Local security. Designed for Snapdragon."
