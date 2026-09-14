# SnapShield AI v1.0.0 — Competition Build

Recommended Git tag: `v1.0.0-competition`

## Overview

SnapShield AI is a privacy-first, local-first multimodal cyber-defense copilot for suspicious messages, URLs, screenshots, QR codes, and sensitive information. It turns local evidence into a bounded risk score, explanation, and recommended action without requiring cloud AI or navigating to submitted URLs.

## Core features

- Local message analysis using a compact ONNX classifier plus deterministic social-engineering signals.
- Structural URL forensics and controlled brand/domain mismatch detection.
- Local RapidOCR extraction and OpenCV QR decoding.
- PII and secret-pattern detection with redaction by default.
- Explainable evidence fusion, recommendations, sanitized local incidents, and runtime reporting.

## Verified ML evidence

The message classifier was evaluated on the fixed 766-message held-out split of the deduplicated UCI SMS Spam Collection: 98.17% accuracy, 95.37% macro F1, 86.67% spam recall, and 0.30% false-positive rate. These are dataset-specific SMS classifier metrics, not universal phishing-detection accuracy.

Dataset: UCI SMS Spam Collection, DOI `10.24432/C5CC84`, CC BY 4.0. The prepared corpus retained 5,105 of 5,574 original messages after duplicate removal.

## ONNX and runtime status

- FP32 ONNX class agreement: 100% across all 766 held-out samples.
- Current verified provider: `CPUExecutionProvider`.
- Recorded median full text pipeline: 5.09 ms on the current development CPU; not a Snapdragon result.
- QNN execution path, provider abstraction, exact-artifact gate, and QDQ candidate: implemented.
- Snapdragon NPU hardware validation: pending. No Snapdragon performance or power result is claimed.

## Testing

- 77 backend tests passed.
- Frontend lint, strict TypeScript, and production build passed.
- Packaged evaluator flow verified for text, URL, OCR, QR, PII, incidents, statistics, runtime, benchmark, and SPA assets.

## How to run

Run `release/SnapShieldAI/SnapShieldAI.exe` and keep its `_internal` directory beside it. The unsigned AMD64 one-folder build opens on `http://127.0.0.1:8765` and stores runtime data beneath `%LOCALAPPDATA%/SnapShieldAI`.

For source setup, follow `QUICKSTART.md`.

## Known limitations

- Primary training data is older English SMS spam, not a complete modern phishing corpus.
- The spam false-negative rate is 13.33% on the fixed test split; low risk is not proof of safety.
- URL analysis intentionally omits live reputation, DNS, redirect expansion, and navigation.
- OCR quality depends on source resolution and layout.
- The Windows artifact is AMD64 and unsigned; native ARM64 packaging and code signing are pending.
- Compatible-device QNN/HTP execution has not been verified.
