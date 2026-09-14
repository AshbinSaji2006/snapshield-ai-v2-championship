# Demo Recording Run Sheet

Target: **3:35**, 1920 × 1080, 100% browser zoom. Full narration is in `FINAL_DEMO_VIDEO_SCRIPT.md`.

Current preflight: the packaged app is responding `ok`, reports `CPUExecutionProvider`, reports Snapdragon NPU verification as false, and all required demo images, presentation files, and screenshot fallbacks exist. Synthetic incident history is non-empty and suitable for the incident view. The detected logical desktop area is not 1920 × 1080, so recording canvas/output and zoom still require human adjustment. Notification state and private desktop visibility also require a human visual check.

## BEFORE RECORDING

- Set the recorder output to 1920 × 1080 at 30 fps or better. The currently detected logical desktop area is 1707 × 1067, so verify the recorder canvas/output explicitly before the take.
- Disable notifications and close personal windows, terminals, developer tools, email, and password managers.
- Confirm the presentation, PDF, and `release/final_submission/screenshots/` fallback folder are openable.
- Keep existing incident history; do not clear it. Use only the built-in synthetic demos.

## START APPLICATION

Run `release/SnapShieldAI/SnapShieldAI.exe`. Confirm **LOCAL PROCESSING**, `CPUExecutionProvider`, and presentation mode. Hold the dashboard for three seconds.

## SCENE 1 — 0:00–0:15 — HERO

Show **Overview**. Point beside the title, local status, and provider. Expected: clean dashboard and real incident analytics. Fallback: `release/final_submission/screenshots/01_snapshield_dashboard.png`.

## SCENE 2 — 0:15–0:35 — LOCAL-FIRST IDEA

Insert `release/final_submission/graphics/09_architecture.png` in the edit, or briefly show the architecture slide. Trace inputs → local engines → fusion → recommendation. Fallback: the same PNG.

## SCENE 3 — 0:35–0:55 — LEGITIMATE

Navigate **Analyze → Message → Legitimate → Analyze locally**. Expected: LOW risk with evidence, live time, and CPU provider. Fallback: `release/final_submission/screenshots/02_legitimate_analysis.png`.

## SCENE 4 — 0:55–1:25 — PHISHING

Click **Bank phish → Analyze locally**. Point to critical/high risk, urgency, credential request, OTP, structural URL evidence, and recommendation. Expected: multiple corroborating indicators; URL never opened. Fallback: `release/final_submission/screenshots/03_phishing_analysis.png`.

## SCENE 5 — 1:25–2:05 — MULTIMODAL

Click **Screenshot** to load `data/samples/demo_multimodal.png`, then **Analyze locally**. Point to OCR text, QR payload, detected destination, **NEVER OPENED**, fused risk, and evidence. Expected: high/critical multimodal result. Fallback: `release/final_submission/screenshots/04_multimodal_screenshot_analysis.png`.

## SCENE 6 — 2:05–2:30 — QR

Click **QR** to load `data/samples/demo_qr.png`, then analyze. Point to decoded payload, URL analysis, risk, and recommendation. Expected: high/critical risk and no navigation. Fallback: `release/final_submission/screenshots/05_qr_analysis.png`.

## SCENE 7 — 2:30–2:45 — PII

Click **PII guard → Analyze locally**. Keep the masked view visible; never click **Show original**. Expected: detected and redacted synthetic email/card/password patterns. Fallback: `release/final_submission/screenshots/06_pii_redaction.png`.

## SCENE 8 — 2:45–3:05 — METRICS

Insert slide 5. Say 5,105 deduplicated UCI SMS messages, 98.17% held-out accuracy, 95.37% macro F1, and 77 tests. State that the accuracy is dataset-specific. Fallback: page 5 of `release/final_submission/SnapShield_AI_Final_Presentation.pdf`.

## SCENE 9 — 3:05–3:25 — SNAPDRAGON PATH

Navigate **Runtime**. Point to `CPUExecutionProvider`, ONNX status, and Snapdragon NPU awaiting hardware validation. Fallback: `release/final_submission/screenshots/08_runtime_benchmarks.png`.

## SCENE 10 — 3:25–3:35 — CLOSE

Return to **Overview** and hold. End with: “Checking whether something is dangerous should not require giving it away first.” Fallback: page 8 of `release/final_submission/SnapShield_AI_Final_Presentation.pdf`.

## STOP RECORDING

Hold the final frame for two seconds, stop cleanly, and save a lossless/high-quality master before editing.

## AFTER RECORDING

- Remove waits and accidental movement; use straight cuts or short dissolves.
- Check against `DEMO_VIDEO_QA_CHECKLIST.md`.
- Export the final MP4, play it end-to-end locally, then add its SHA-256 to the final checksum manifest.
