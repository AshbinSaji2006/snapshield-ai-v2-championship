# SnapShield AI — Presentation Day Card

## Opening sentence

“Suspicious security content can expose the very data people are trying to protect.”

## Three numbers to remember

- **5,105** — retained, deduplicated UCI SMS messages.
- **95.37%** — macro F1 on the fixed held-out UCI SMS test split.
- **77** — backend tests passed.

If mentioning **98.17%**, always say: “held-out accuracy on the deduplicated UCI SMS Spam Collection.”

## Main architecture message

Messages, URLs, screenshots, and QR codes enter specialized local engines. Text ML, URL forensics, OCR, QR, PII, brand checks, and security rules become one explainable risk assessment and recommendation. Raw submitted content stays out of persistent incident history.

## Snapdragon wording

“Designed for Snapdragon-powered PCs. QNN execution path implemented; hardware validation pending. Current verified provider: CPUExecutionProvider. No Snapdragon performance or power result is claimed.”

## Most dangerous judge question

**“Is this actually running on Snapdragon?”**

**Answer:** “The current competition build is verified on CPUExecutionProvider. The application uses ONNX Runtime with provider abstraction, and the QNN execution path plus exact-artifact validation gate are implemented. I did not have compatible Snapdragon hardware available, so I am explicitly not claiming NPU performance. Hardware validation is the next deployment step.”

## Closing sentence

“Our next measurable milestone is verified QNN execution on compatible Snapdragon hardware.”

## Demo recovery

- Launch: `release/SnapShieldAI/SnapShieldAI.exe`
- Real screenshot fallback: `docs/final_submission/assets/screenshots/`
- Presenter script: `release/final_submission/FINAL_PRESENTER_SCRIPT.md`
- If OCR/QR stalls, switch to the matching real screenshot and state that it is captured application evidence.
