# SnapShield AI — Project Summary

**Private On-Device Multimodal Cyber Defense for Snapdragon PCs**

SnapShield AI is a privacy-first, local-first cyber-defense copilot for suspicious messages, URLs, screenshots, and QR codes. It combines a compact local text classifier with URL structural forensics, social-engineering indicators, OCR, QR decoding, controlled brand/domain checks, PII detection and redaction, deterministic security rules, and evidence-based risk fusion. It returns a bounded risk score, the evidence behind it, and a practical recommendation. Submitted URLs are parsed but never opened, and incident history stores hashes plus sanitized derived metadata rather than raw content.

## Verified evidence

- 5,105 retained, deduplicated messages from the UCI SMS Spam Collection.
- Fixed 766-message held-out test split.
- 98.17% held-out accuracy and 95.37% macro F1 on that dataset-specific test set.
- 86.67% spam recall, 0.30% false-positive rate, and 13.33% false-negative rate.
- 100% FP32 ONNX class agreement across all 766 held-out samples.
- 77 backend tests passed.
- 5.09 ms median full text pipeline on the current development CPU.
- Packaged Windows evaluator flow verified with `CPUExecutionProvider`.

These classifier figures do not represent universal phishing detection accuracy. The classifier is one signal inside the broader multimodal pipeline.

## Snapdragon status

SnapShield uses ONNX Runtime and implements provider abstraction, a QNN execution path, exact-artifact validation, and a calibrated QDQ candidate. Current verified execution is `CPUExecutionProvider`. The architecture is designed for Snapdragon-powered PCs; QNN/Snapdragon NPU hardware validation is pending. No Snapdragon performance, power, thermal, or battery result is claimed.

## Submission package

The judge-facing release contains an eight-slide PPTX and synchronized PDF, eight real 1920 × 1080 application screenshots, architecture and privacy visuals, presenter and demo scripts, a recording guide, submission answers, and integrity checksums. A real demo video must still be recorded by the submitter using the supplied runbook.
