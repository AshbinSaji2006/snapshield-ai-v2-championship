# Final Portal Answers

Copy only the field requested. Character limits were not visible on the public challenge page, so verify each logged-in field before pasting.

## Project Name

SnapShield AI

## Tagline

Your data never needs to leave your device to protect your device.

## Problem

Suspicious messages, links, screenshots, and QR codes may contain banking context, credentials, or personal information. Cloud-dependent analysis may add another privacy boundary, while users still need clear evidence and a safe next action.

## Solution

SnapShield AI analyzes suspicious content locally. A compact ONNX message classifier works with URL forensics, social-engineering indicators, OCR, QR decoding, PII redaction, brand/domain checks, and deterministic security rules. Evidence fusion returns a bounded risk score, explanation, and recommendation. URLs are parsed but never opened, and incident history excludes raw submitted content.

## Innovation

SnapShield is not a single spam classifier. Its innovation is a local multimodal evidence pipeline with transparent signal-level explanations, privacy-minimal persistence, and runtime reporting that distinguishes implemented accelerator support from verified execution.

## Use of AI

The learned component is a versioned word unigram/bigram TF-IDF logistic-regression classifier exported to ONNX. RapidOCR contributes locally extracted text. Deterministic engines complement the model for URL structure, persuasion, evasion, PII, QR, and controlled brand/domain evidence.

## Dataset

UCI SMS Spam Collection, DOI `10.24432/C5CC84`, licensed CC BY 4.0. The source contained 5,574 messages; deterministic exact and normalized duplicate removal retained 5,105 before the fixed train/validation/test split.

## Model

SnapShield UCI SMS Word TF-IDF Logistic Regression v2.0.0. The production FP32 ONNX graph uses MatMul, Add, and Sigmoid and is executed through ONNX Runtime.

## Metrics

On the fixed 766-message held-out split of the deduplicated UCI SMS Spam Collection, the classifier achieved 98.17% accuracy, 95.37% macro F1, 86.67% spam recall, and a 0.30% false-positive rate. FP32 ONNX class agreement was 100% across all 766 samples. These are dataset-specific classifier results, not universal phishing-detection accuracy.

## Snapdragon Relevance

Designed for Snapdragon-powered PCs. SnapShield has a Snapdragon-ready ONNX/QNN deployment architecture, provider abstraction, an implemented QNN execution path, an exact-artifact validation gate, and a QDQ candidate. Current verified provider: `CPUExecutionProvider`. QNN/Snapdragon NPU hardware validation is pending; no Snapdragon performance or power result is claimed.

## Deployment

The verified competition artifact is an unsigned Windows AMD64 one-folder application. It binds to loopback, runs the core pipeline locally, works without cloud AI, and reports the selected execution provider. Native ARM64 packaging and code signing are pending.

## Impact

SnapShield reduces the need to send sensitive security evidence to a remote AI service and helps users understand why content is risky across several threat surfaces. Its offline core supports use during connectivity loss and makes the decision trail inspectable.

## Privacy

Analysis is local and cloud AI is disabled. Submitted URLs are never visited. Raw messages, images, full URLs, credentials, tokens, and extracted PII are excluded from persistent incident records; sensitive values are masked in results by default.

## Future Roadmap

First: validate QNN/HTP execution on compatible Snapdragon hardware with CPU fallback disabled and exact artifact verification. Then produce a native ARM64 signed package, broaden modern and multilingual evaluation, and conduct external security review.

## Repository Link

`PUBLIC_REPOSITORY_URL_PENDING`

## Demo Video Link

`DEMO_VIDEO_URL_PENDING`
