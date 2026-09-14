# Demo Failure Plan

The recovery goal is not to hide a failure. It is to preserve the story, disclose what happened, and continue with verified evidence.

## Before entering the room

- Launch the packaged application once and confirm **Local AI active**.
- Confirm the provider shown in the header and Runtime page.
- Run **Legitimate**, **Bank phish**, **Screenshot**, and **PII guard** once.
- Confirm the bundled assets load without browsing for files.
- Disable notifications, screen savers, VPN prompts, automatic updates, and presentation overlays.
- Keep the laptop on power. Carry a local MP4 recording, eight PNG screenshots, a PDF of the deck, the installer/portable package, and this plan.
- Never depend on venue Wi-Fi; the product demo is local.

## Recovery ladder

### 1. A click or input fails

Click **Reset**, choose the built-in demo chip again, and retry once. Say: “I’m resetting the local input state and retrying the bundled synthetic sample.” Do not repeatedly click while the analysis is running.

### 2. The local API is offline

If the header says **Local AI offline**, wait five seconds. Relaunch the packaged application once. If it remains offline, switch immediately to the prerecorded demo and say: “The local service did not start in this session, so I’ll show the same pre-recorded build rather than imply a successful live run.”

### 3. OCR or image analysis is slow

Allow up to 20 seconds for the bundled screenshot. Continue speaking about the three local stages: OCR, QR decoding, and evidence fusion. If there is still no result, switch to the saved screenshot of that result and disclose the timeout. Do not restart more than once.

### 4. The output differs from rehearsal

Show the actual result. Describe the visible evidence, not the expected label. If a core result is materially wrong, say: “This live sample produced an unexpected result; the evaluation report and prerecorded run are reproducible artifacts, and this edge case would enter our error analysis.” Do not manipulate the input until it passes.

### 5. QNN is unavailable

This is expected on non-Snapdragon hardware. Show the Runtime page and say: “CPU fallback is active and truthfully reported. The QNN path is implemented but remains unverified until we run it on compatible Snapdragon hardware.” Never disguise CPU inference as NPU inference.

### 6. Projector or resolution fails

Use the PDF deck and the prerecorded 1080p demo from a second local player. If only the app is visible, enable **Presentation mode** and use browser zoom between 90% and 110%. Avoid changing Windows display scaling during the presentation.

### 7. Laptop fails completely

Move to the backup laptop or play the local MP4 from a USB drive. Use screenshots for Q&A. State that these are captured results from the verified build, not a live execution.

## Required offline evidence pack

Keep these files in one folder named `SnapShield_Demo_Backup`:

1. `SnapShield_Deck.pdf`
2. `SnapShield_Demo_1080p.mp4`
3. `01_overview.png` through `08_incident_privacy.png`
4. `SUBMISSION_FACTS.pdf`
5. `evaluation_report.json`
6. `onnx_equivalence_report.json`
7. `runtime_report.json`
8. Packaged application and its SHA-256 text file

The screenshots and video must be captured from the actual build; do not create simulated UI results.

## One-line bridge back to the pitch

“The live environment changed, but the product principle did not: measured evidence is reported exactly, and unverified acceleration is never claimed.”
