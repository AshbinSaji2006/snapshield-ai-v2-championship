# Four-minute demo guide

Use the header's Presentation mode. Every quick demo invokes the real local pipeline.

1. **0:00-0:25 - Problem.** Private emails and screenshots are exactly the material users should not have to upload to a generic cloud service.
2. **0:25-0:45 - Architecture.** Point to Local processing and the exact AI Runtime provider. Say the verdict combines ML with inspectable security evidence.
3. **0:45-1:15 - Legitimate versus phishing.** Run the legitimate professional sample, then Bank phishing. Contrast LOW with the phishing score; expand urgency, credential, URL, and brand/domain evidence.
4. **1:15-1:55 - Flagship screenshot.** Choose Screenshot. Show local RapidOCR text, one decoded QR, extracted URL, PII, score, and specific explanation.
5. **1:55-2:20 - QR attack.** Choose QR image. Emphasize that pixels are decoded locally and the URL is analyzed but never opened.
6. **2:20-2:40 - PII.** Run Sensitive data and show masking; explain that raw input is not persisted.
7. **2:40-3:10 - Runtime.** Show ONNX primary, `CPUExecutionProvider`, NPU awaiting hardware validation, and the separated benchmark. Do not claim NPU speed.
8. **3:10-3:30 - Forensics and close.** Open one incident, show sanitized evidence/model/runtime/latency, delete it, and close on private offline defense.

Safe assets are in `data/samples`: legitimate, bank/delivery phishing, obfuscated URL, PII, clear screenshot, low-resolution screenshot, multimodal screenshot+QR, and QR-only image.

## Screenshot capture workflow

Build and launch at 100% browser zoom on a 1920x1080 display. Enable Presentation mode. Capture actual UI states in this order:

1. Overview hero with Local processing and AI Runtime visible.
2. Bank phishing result with score, severity, and evidence.
3. Multimodal screenshot result with OCR and QR details.
4. QR-only result with decoded structural URL findings.
5. Sensitive-data result with redacted view.
6. Analytics after the demo sequence.
7. Runtime panel plus measured benchmark.
8. Architecture diagram rendered from `ARCHITECTURE.md`.

Save final captures under `docs/screenshots`. Do not crop away provider/status labels and do not use mocked data. Screenshots remain pending because no GUI capture tool was available in this automated environment.
