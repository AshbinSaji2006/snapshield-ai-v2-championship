# SnapShield AI v2 — submission portal answers

## Project name

SnapShield AI

## Subtitle

Adaptive Private On-Device Multimodal Cyber Defense for Snapdragon PCs

## Tagline

Your data never needs to leave your device to protect your device.

## Short description

SnapShield AI is a local-first Windows cyber-defense copilot for suspicious messages, URLs, screenshots, and QR codes. A calibrated Fast Guard and compact BERT Tiny Deep Guard are adaptively routed alongside local OCR, QR decoding, URL/domain forensics, PII analysis, brand/domain checks, transparent security rules, and a Threat Evidence Graph. The result is an explainable risk and safe action without visiting submitted destinations or requiring cloud AI.

## Technical evidence

On the untouched 766-message UCI SMS test, Deep Guard reached 98.56% accuracy and 94.44% positive recall. On an independently sourced, strictly UCI-deduplicated 521-message 2022 Mendeley holdout, it reached 98.85% accuracy and 98.04% recall. Adaptive v2.2 matched UCI Deep Guard recall, produced a 0.30% false-positive rate, and escalated 33.68% of UCI inputs. These are named SMS dataset results, not universal phishing accuracy.

The repository has 100 passing backend tests and 20/20 curated functional robustness checks. The final AMD64 CPU benchmark measured a 28.69 ms median full deep-routed text pipeline. OCR measured 3,304.17 ms median and remains the dominant multimodal cost. These are development-PC measurements, not Snapdragon results.

## Snapdragon relevance

The current verified runtime is ONNX Runtime with `CPUExecutionProvider`. The architecture implements provider discovery, an explicit strict QNN path, exact-artifact hash gating, a static QDQ candidate, and Qualcomm AI Hub compile/profile automation targeting Snapdragon X Elite CRD. QNN/Snapdragon NPU hardware validation is pending. No NPU latency, power, battery, TOPS, or native ARM64 claim is made.

## Privacy and security

Core analysis runs locally after installation. URLs are parsed but never visited. Raw messages and images are excluded from incident history. Live Shield is off by default, requires explicit consent, rate-limits and deduplicates clipboard checks, and stores an incident only when requested. The separate developer-triggered AI Hub workflow may upload a model artifact after authentication; it never handles user content and is not part of production analysis.

## Repository

<https://github.com/AshbinSaji2006/snapshield-ai-v2-championship>

## Demo video

`DEMO_VIDEO_URL_PENDING`
