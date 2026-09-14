# Final Demo Video Script

Target runtime: **3:35**. This is the production script unless the competition portal publishes a different limit. All threat content is synthetic and inert; show only real application outputs.

## 0:00–0:15 — Hero and problem

**Picture:** Dashboard at 1920 × 1080. Hold long enough to read **LOCAL PROCESSING** and **CPUExecutionProvider**.

**Narration:** "SnapShield AI is private, on-device, multimodal cyber defense. Suspicious content can itself be sensitive, so the core analysis runs locally instead of requiring cloud AI."

**On-screen caption:** `YOUR DATA NEVER NEEDS TO LEAVE YOUR DEVICE TO PROTECT YOUR DEVICE.`

**Cut:** Clean cut after selecting **Analyze**.

## 0:15–0:35 — Local architecture

**Picture:** Use `09_architecture.png`; animate only a slow left-to-right pan if desired.

**Narration:** "Messages, URLs, screenshots, and QR codes pass through specialized local engines. OCR, QR decoding, URL forensics, the ONNX text model, privacy checks, and security rules become one explainable risk assessment and recommendation."

**On-screen caption:** `LOCAL-FIRST • MULTIMODAL • EXPLAINABLE`

## 0:35–0:55 — Legitimate message

**Picture:** Click **Legitimate**, then **Analyze locally**. Point to the live low-risk result, evidence, elapsed time, and provider.

**Narration:** "A normal university meeting message returns low risk. SnapShield does not treat every message as malicious, and it still shows the evidence, live processing time, and local runtime."

**Rule:** Do not narrate an exact live score or latency; read only what the application displays.

## 0:55–1:25 — Phishing message

**Picture:** Click **Bank phish**, then **Analyze locally**. Pause on the critical result, explanation, evidence trail, and recommended action.

**Narration:** "This synthetic bank lure combines urgency, an account threat, credential and one-time-code requests, and a numeric-host URL on a nonstandard port. SnapShield fuses those independent signals into a bounded risk score, explains why it was flagged, and recommends a safe next step. The URL is parsed, never opened."

**On-screen caption:** `RISK IS EVIDENCE-WEIGHTED—NOT A CALIBRATED PROBABILITY.`

## 1:25–2:05 — Multimodal screenshot

**Picture:** Click **Screenshot** to load `demo_multimodal.png`, then **Analyze locally**. Move the pointer from the uploaded filename to OCR text, QR payload, detected destination, **NEVER OPENED**, overall risk, and evidence.

**Narration:** "Now the same attack pattern is inside an image. Local OCR extracts the visible message. The QR decoder recovers its destination without navigating to it. Text, URL, QR, PII, and brand-domain evidence are correlated in one result. This real pipeline is why SnapShield is more than a text classifier."

**On-screen caption:** `REAL OCR + REAL QR DECODE + EXPLAINABLE FUSION`

## 2:05–2:30 — QR security

**Picture:** Click **QR**, analyze, and show the decoded payload, structural URL findings, score, and recommendation.

**Narration:** "A QR code is treated as an untrusted container. SnapShield decodes it locally, displays the destination, performs structural URL analysis, and never automatically opens the link."

**On-screen caption:** `DECODED LOCALLY • NEVER OPENED`

## 2:30–2:45 — PII redaction

**Picture:** Click **PII guard**, analyze, and keep the default redacted view visible.

**Narration:** "Privacy is part of the defense. Sensitive patterns are detected and masked in the result, while incident history excludes submitted source content and extracted PII."

## 2:45–3:05 — Verified engineering results

**Picture:** Use slide 5 or a clean crop of it.

**Narration:** "The compact text component retained 5,105 deduplicated UCI SMS messages. It achieved 98.17 percent held-out accuracy and 95.37 percent macro F1 on that dataset's fixed test split—not universal phishing accuracy. FP32 ONNX class agreement is 100 percent across 766 held-out samples, and 77 backend tests pass."

**On-screen footnote:** `UCI SMS Spam Collection test set; these metrics do not represent universal phishing detection accuracy.`

## 3:05–3:25 — Snapdragon deployment path

**Picture:** Open **Runtime**. Point to **CPUExecutionProvider**, QNN path status, and Snapdragon validation status.

**Narration:** "This machine truthfully reports CPUExecutionProvider. The Snapdragon-ready ONNX and QNN deployment path is implemented, including provider abstraction and artifact validation, but Snapdragon NPU hardware validation is still pending. No NPU performance or power claim is being made."

**On-screen caption:** `CPU VERIFIED • QNN HARDWARE VALIDATION PENDING`

## 3:25–3:35 — Close

**Picture:** Return to the dashboard or use slide 8.

**Narration:** "SnapShield AI: private AI, local security, designed for Snapdragon. Checking whether something is dangerous should not require giving it away first."

## Edit notes

- Use straight cuts or very short dissolves; remove waits and loading dead time.
- Keep the product UI dominant. Do not add stock threat imagery or simulated results.
- Captions should use the deck's mint, off-white, and amber palette.
- Do not use copyrighted commercial music. Silence or a subtle properly licensed bed is acceptable.
- Normalize narration, but preserve audible click feedback only when it helps orientation.

## What not to claim

- Do not call 98.17% universal phishing accuracy; it is held-out accuracy on the deduplicated UCI SMS Spam Collection.
- Do not say Snapdragon NPU verified, powered by Snapdragon NPU, NPU accelerated, QNN validated, or Snapdragon optimized.
- Do not call the fused risk score a probability.
- Do not claim measured Snapdragon latency, power, thermal, or battery improvement.
- Do not promise an exact live risk score, OCR time, or benchmark value.
