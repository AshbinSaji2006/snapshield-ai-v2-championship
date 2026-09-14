# Final Video Recording Guide

This runbook records the real packaged application without fabricated states. Follow the narration and timing in `FINAL_DEMO_VIDEO_SCRIPT.md`.

## Capture setup

- Record at **1920 × 1080**, 16:9, 30 fps or better.
- Use Microsoft Edge or the desktop shell maximized, presentation mode enabled, and **100% zoom** for every take.
- Use an already available recorder such as OBS Studio, Windows Snipping Tool screen recording, or Xbox Game Bar.
- Use the standard cursor with no trails. Move slowly and park beside labels, never over text.
- Close terminals, developer tools, notifications, password managers, personal tabs, and debug windows.
- Record narration separately if that produces cleaner pacing.

## Start the application

1. Run `release/SnapShieldAI/SnapShieldAI.exe`.
2. Wait for the dashboard and confirm **LOCAL PROCESSING** and **CPUExecutionProvider**.
3. Enter presentation mode.
4. Run each built-in sample once off-camera. Do not promise an exact live score or latency.
5. Return to **Overview**, hold for three seconds, and start the final recording.

## Sample and cursor order

1. **Overview:** show the product name, local status, runtime provider, privacy promise, and main analysis surfaces.
2. **Legitimate:** select the chip, click **Analyze locally**, then point to low risk, evidence, processing time, and provider.
3. **Bank phish:** select the chip, analyze, then point to severity, explanation, urgency, credential request, OTP, URL evidence, and recommendation.
4. **Screenshot:** select `demo_multimodal.png`, analyze, then point to overall risk, OCR text, QR payload, detected destination, **NEVER OPENED**, and evidence.
5. **QR:** select the QR demo, analyze, then point to decoded data, destination, structural URL evidence, and recommendation.
6. **PII guard:** select the chip, analyze, and leave the default masked view visible. Do not use **Show original** in the judged take.
7. **Runtime:** point to `CPUExecutionProvider`, ONNX model status, and Snapdragon NPU awaiting hardware validation.
8. **Overview:** return to the clean dashboard and hold for four seconds before stopping.

## Validated inert assets

- Legitimate message: `Hi Priya, the university design review is confirmed for Tuesday at 2 PM in Lab 4. No action is needed before the meeting.`
- Bank-themed lure: `SBI SECURITY ALERT: Your account has been suspended. Verify your password and OTP immediately at http://192.0.2.1:8080/sbi/verify/login.exe`
- PII test: `Contact priya@example.com. Example card 4111 1111 1111 1111. password=not-a-real-secret`
- Multimodal screenshot: `data/samples/demo_multimodal.png`
- QR image: `data/samples/demo_qr.png`

Never substitute an active malicious link, a real credential, or personal data.

## Cut and voice-over timing

- Follow the 3:35 sequence in `FINAL_DEMO_VIDEO_SCRIPT.md`.
- Cut immediately before a chip selection and after the result settles.
- Remove analysis waits, accidental scrolling, repeated clicks, and navigation dead time.
- Leave at least two seconds on each result and four seconds on architecture and metric frames.
- Use straight cuts or very short dissolves. Keep the application visually dominant.

## Failure recovery

- **OCR stalls or fails:** stop the take, relaunch, and retry the bundled `demo_multimodal.png` once. If it still fails, use the already captured real `04_multimodal_screenshot_analysis.png` while clearly narrating it as recorded application evidence.
- **QR stalls or fails:** retry `data/samples/demo_qr.png` once. Otherwise use the real `05_qr_analysis.png` capture and continue the narration.
- **Packaged build does not start:** verify port 8765 is free, close an earlier SnapShield process, and relaunch. If it remains unavailable, record the validated source build and state that the displayed provider is the one reported on screen.
- **Live demo interruption:** switch to the eight real screenshots in `assets/screenshots/` in the source tree or `screenshots/` in the release bundle; never simulate a click or fabricate a model response.

## Expected output contract

- Legitimate: low risk.
- Bank phish: high or critical with urgency, credential/OTP, and URL evidence.
- Screenshot: OCR plus QR/destination evidence and a fused high or critical result.
- QR: decoded payload and URL analysis with no automatic navigation.
- PII: masked sensitive findings.
- Runtime: `CPUExecutionProvider`; QNN/Snapdragon NPU hardware validation pending.

Live values may vary. Record the values actually produced in the take.
