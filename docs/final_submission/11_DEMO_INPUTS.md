# Safe Demo Inputs

All inputs below are synthetic. `.example` domains and `192.0.2.1` are intentionally non-production identifiers. SnapShield must parse URLs, never visit them.

## A. Benign control

Use the built-in **Legitimate** chip:

> Hi Priya, the university design review is confirmed for Tuesday at 2 PM in Lab 4. No action is needed before the meeting.

Purpose: show that the system can return a low-risk result instead of flagging every message.

## B. Bank-themed phish

Use the built-in **Bank phish** chip:

> SBI SECURITY ALERT: Your account has been suspended. Verify your password and OTP immediately at http://192.0.2.1:8080/sbi/verify/login.exe

Purpose: demonstrate urgency, credential requests, a numeric host, nonstandard port, suspicious path terms, and fused evidence.

## C. Obfuscated delivery lure

Use the built-in **Obfuscated** chip:

> Your parcel is held. Pay the fee now at hxxp://delivery-update[.]example/pay.

Purpose: demonstrate safe handling of defanged/obfuscated indicators and social-engineering language.

## D. Privacy guard

Use the built-in **PII guard** chip:

> Contact priya@example.com. Example card 4111 1111 1111 1111. password=not-a-real-secret

Purpose: demonstrate local PII/secret-pattern detection and redaction. The card number is a standard non-financial test value, and the password is explicitly fake.

## E. URL-only analysis

Select the **URL** tab and paste:

> http://192.0.2.1:8080/verify/account/login.exe

Purpose: demonstrate structural URL inspection without navigation or reputation lookup.

## F. Bundled images

| UI chip | Repository asset | Demonstrates |
|---|---|---|
| Screenshot | `data/samples/demo_multimodal.png` | Synthetic phishing screenshot, local OCR, embedded QR, and evidence fusion |
| QR | `data/samples/demo_qr.png` | QR decoding and URL analysis |
| Manual fallback | `data/samples/demo_screenshot.png` | OCR-only synthetic phishing screenshot |
| Stress sample | `data/samples/demo_low_resolution.jpg` | Lower-resolution OCR behavior; use outside the timed demo |

## Demo rules

- Use the built-in chips first; they prevent typing errors.
- Do not use a real bank domain, active malicious URL, real credential, or personal data.
- Do not promise an exact live risk score or latency. Show the value that actually appears.
- If a sample behaves unexpectedly, preserve honesty and switch to the prerecorded evidence described in the failure plan.
