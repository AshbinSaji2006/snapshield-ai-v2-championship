# Changelog

## 2.0.0 Final Competition Hardening - 2026-09-12

- Replaced prototype ML claims with the licensed UCI SMS Spam Collection, pre-split deduplication, three-candidate validation, untouched test metrics, and plots.
- Exported/validated FP32 and QDQ ONNX artifacts; made ONNX Runtime primary with local fallback.
- Added RapidOCR local OCR, end-to-end OCR+QR multimodal analysis, safe demo assets, and component benchmarks.
- Added Unicode/defanged URL handling, controlled brand-domain mismatch, evidence spans, explanation improvements, and 18 adversarial cases.
- Expanded to 77 backend tests and hardened origins, hosts, headers, uploads, asset routing, QNN artifact gating, storage, and error behavior.
- Added presentation mode, one-click real demos, truthful runtime details, and incident forensics.
- Added automated Snapdragon validation and an unsigned, smoke-tested Windows one-folder package.

## 1.0.0 Competition Build - 2026-09-11

- Added the initial local text, URL, PII, risk, incident, runtime, image/QR, React UI, and documentation paths.
