# 3.5-minute technical demo

**0:00-0:25 - Problem.** "Messages and screenshots used for cyber defense often contain passwords, account context, or personal data. SnapShield analyzes them locally instead of creating a cloud disclosure boundary."

**0:25-0:45 - Architecture.** Show Local processing and AI Runtime. "A trained ONNX classifier is supporting evidence. URL, text, Unicode, brand, PII, OCR, and QR engines produce inspectable findings; a bounded policy fuses them."

**0:45-1:15 - Legitimate vs phishing.** Run Legitimate, then Bank phishing. Point to the score, severity, exact urgency/credential wording, suspicious hostname, and SBI domain mismatch.

**1:15-1:55 - Flagship multimodal.** Run Screenshot. "RapidOCR extracts the message locally, OpenCV decodes the QR, both enter the same text/URL/PII pipeline, and results are generated now - not hardcoded."

**1:55-2:20 - QR threat.** Run QR image. Show the decoded link and IP/port/path indicators. "SnapShield never opens the destination."

**2:20-2:40 - PII.** Run Sensitive data and show redaction. "The source is not saved; history contains only a hash and sanitized evidence."

**2:40-3:10 - Snapdragon/runtime.** Show `CPUExecutionProvider`. "The 41 KB ONNX graph and 12 KB QDQ candidate are implemented. QNN is awaiting real ARM64 hardware validation, so I make no NPU speed claim." Mention 0.080 ms median ONNX-only CPU inference and 1.86 s median full multimodal processing.

**3:10-3:30 - Close.** Open a sanitized incident and delete it. "SnapShield turns private, multimodal threat evidence into an explainable action while keeping the content on the PC."
