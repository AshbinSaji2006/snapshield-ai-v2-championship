# Exact Live Demo Script

Target duration: **2 minutes 20 seconds**. Use the packaged desktop build, a 1920×1080 display, 100% Windows scale, and the browser/app at 90–100% zoom. Open SnapShield before the judges arrive and wait until the header reads **Local AI active**.

## Pre-demo state

- Use the bundled synthetic samples only. They contain reserved `.example` domains and documentation-only IP address `192.0.2.1`.
- Open **Overview**, then enable **Presentation mode**.
- Confirm **AI runtime** displays the actual selected provider. On the development laptop this is `CPUExecutionProvider`.
- Keep `docs/final_submission/12_DEMO_FAILURE_PLAN.md` open on the presenter laptop, not on the projected screen.

## Click-by-click run

### 0:00–0:15 — Establish the promise

1. Show **Overview**.
2. Point to **Local AI active**, **AI runtime**, and **Local processing** in the header.
3. Say: “SnapShield inspects suspicious messages, links, and screenshots through a local, explainable pipeline. The runtime badge reports what this machine is actually using.”
4. Do not say: “This laptop is using the Snapdragon NPU” unless the live Runtime page explicitly verifies QNN execution.

### 0:15–0:50 — Benign control

1. Click **Start local analysis**.
2. Click the **Legitimate** demo chip.
3. Click **Analyze locally**.
4. Let the assessment finish; do not narrate a promised score before it appears.
5. Point to the risk ring, the category, **No strong indicators detected** when shown, and the local provider label.
6. Say: “A security system must distinguish ordinary communication from manipulative content. This control demonstrates that the interface reports evidence rather than labeling everything dangerous.”

Expected result: a low-risk/benign assessment. Exact scores and latency are live outputs and must not be memorized or promised.

### 0:50–1:25 — Text and URL phishing

1. Click **Bank phish**.
2. Click **Analyze locally**.
3. Point to **Why this was flagged**, then two or three entries under **Detected indicators**.
4. Say: “The message combines urgency, credential and OTP requests, and a suspicious numeric-host URL. SnapShield fuses a compact local text model with deterministic social-engineering and URL evidence, then recommends a safe action.”
5. Point to the line stating the input remained local.
6. Do not call the score a calibrated probability. It is an explainable fused risk score.

Expected result: high or critical risk with multiple contributing indicators. The test is fully synthetic; SnapShield parses the URL but never opens it.

### 1:25–1:55 — Multimodal screenshot

1. Click **Screenshot** in the demo strip. This loads bundled `demo_multimodal.png`.
2. Confirm the **Image** tab and file name are visible.
3. Click **Analyze locally**.
4. Point to the screenshot-derived evidence and QR/URL evidence in the result.
5. Say: “This is the same attack pattern inside an image. Local OCR recovers visible text, QR decoding extracts the embedded indicator, and the same evidence-fusion layer explains the outcome.”
6. Do not say that OCR is instant or promise the CPU timing; image processing is intentionally heavier than text analysis.

### 1:55–2:12 — Privacy guard

1. Click **PII guard**.
2. Click **Analyze locally**.
3. In **Sensitive data**, show that the default view is redacted. Do not click **Show original** during the judged demo.
4. Say: “Privacy is part of the defense. Sensitive patterns are masked in the result, while persistent incident records exclude the submitted source and extracted PII.”

### 2:12–2:20 — Hardware honesty

1. Click **Runtime** in the sidebar.
2. Point to **Selected provider** and **Snapdragon NPU**.
3. Say: “The QNN path is implemented, but this x64 machine truthfully reports CPU fallback. We claim Snapdragon NPU execution only after a compatible device produces a verified QNN report.”

## Optional 20-second close

Open **Incident center** and select one row. Say: “The local history keeps only a SHA-256 input hash, score, timing, classification, provider, and sanitized evidence names. Raw messages, images, full URLs, credentials, and extracted PII are not stored.”

## Claims discipline

Say **98.17% test accuracy on the retained UCI SMS Spam Collection evaluation split**. Never shorten that to “98.17% phishing accuracy.” Say **designed for Snapdragon PCs with an implemented QNN path awaiting compatible-device validation** until actual QNN evidence exists.
