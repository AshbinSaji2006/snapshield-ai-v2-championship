# Submission Form Answers

These answers are ready to paste. Choose the length that fits the form; do not combine variants if the field has a strict character limit.

## Project name

SnapShield AI

## Subtitle

Private On-Device Multimodal Cyber Defense for Snapdragon PCs

## Tagline

Your data never needs to leave your device to protect your device.

## Ten-word description

Private multimodal threat analysis designed for local Snapdragon PC inference.

## One-sentence summary

SnapShield AI locally analyzes suspicious messages, URLs, screenshots, QR codes, and sensitive-data exposure, then combines explainable evidence into one actionable risk assessment.

## Short description

SnapShield AI is a privacy-first desktop defense console for suspicious messages, links, and screenshots. It combines a compact ONNX text classifier with URL forensics, social-engineering rules, local OCR, QR decoding, PII redaction, and evidence-weighted risk fusion. Raw source content stays out of persistent history. The current build runs through ONNX Runtime CPU fallback, while an implemented QNN path is ready for verification on compatible Snapdragon hardware.

## Medium description

Phishing and scam evidence increasingly arrives across text, links, screenshots, and QR codes, while cloud-only analysis can expose the same sensitive content users are trying to protect. SnapShield AI is a local-first cyber-defense console designed for Snapdragon PCs. A compact TF-IDF logistic-regression model exported to ONNX evaluates message language; independent engines inspect URL structure, social-engineering cues, OCR text, QR indicators, PII, and brand inconsistencies. An explainable fusion layer turns those signals into a risk score, evidence trail, and recommended actions. The current verified build uses ONNX Runtime CPU fallback on x64 Windows. QNN provider detection, strict no-fallback verification, and quantized artifacts are implemented, but Snapdragon NPU execution remains explicitly unverified until tested on compatible hardware.

## Long description

SnapShield AI addresses a practical gap in everyday cyber defense: suspicious content rarely arrives as clean text alone. It may be a message with a shortened-looking link, an image containing urgent instructions, a QR code leading to a credential page, or content that exposes sensitive data. Sending that evidence to a cloud model may create an additional privacy risk.

SnapShield analyzes the content through a local multimodal pipeline. A compact TF-IDF logistic-regression classifier exported to ONNX estimates spam-like language. Deterministic modules independently inspect social-engineering patterns, URL structure, OCR text, QR payloads, PII and secret patterns, and brand/domain inconsistencies. A transparent fusion layer converts the combined evidence into a bounded risk score, severity, explanation, and recommended next steps. Suspicious URLs are parsed but never visited. Persistent incident history contains only an input hash and sanitized decision metadata—not raw messages, screenshots, full URLs, credentials, or extracted PII.

The text model achieved 98.1723% accuracy and 91.7647% F1 on a fixed 766-message test split of the retained UCI SMS Spam Collection corpus. Those figures are dataset-specific, not a claim of real-world phishing detection accuracy. The verified development runtime is ONNX Runtime CPU execution on an AMD64 Windows machine. The application implements QNN capability detection, an NPU-prepared quantized model, strict no-fallback verification, and CPU fallback, but actual Snapdragon NPU execution remains pending access to compatible hardware.

## Problem

People receive high-pressure scams across messages, URLs, screenshots, and QR codes. Existing workflows often require users to recognize technical warning signs themselves or upload sensitive evidence to a remote service. The evidence is fragmented, the explanations are inconsistent, and privacy becomes a tradeoff.

## Solution

SnapShield performs local, layered inspection and presents one understandable assessment. Compact ML captures message patterns; deterministic engines expose concrete URL, persuasion, OCR, QR, privacy, and brand signals; evidence fusion makes the decision traceable. The architecture is designed to take advantage of Snapdragon PC acceleration while retaining honest CPU fallback.

## Innovation

The innovation is not a single classifier. It is the combination of multimodal local analysis, explicit privacy boundaries, evidence-level explanations, and hardware-verifiable provider reporting. SnapShield refuses to infer NPU use from the device name: it verifies the QNN provider and records the actual execution path.

## Use of AI/ML

SnapShield uses a versioned TF-IDF word unigram/bigram logistic-regression classifier exported as an ONNX graph. The production FP32 artifact has 10,264 input features and contains MatMul, Add, and Sigmoid operations. Local OCR provides text to the same analysis pipeline; deterministic security modules complement rather than conceal the model’s limitations.

## Use of Snapdragon technology

SnapShield is designed around a deployable ONNX pipeline with a QNN execution-provider path, NPU-oriented quantized artifact, provider capability detection, strict no-CPU-fallback verification, artifact hashing, and transparent fallback reporting. On the current non-Snapdragon x64 machine, QNN is unavailable and CPU execution is correctly reported. Compatible-device QNN/HTP validation is the next required hardware milestone.

## Privacy and security

Analysis is local and cloud AI is disabled. URLs are structurally parsed but never opened. Raw messages, images, full URLs, credentials, tokens, and extracted PII are excluded from persistent incident records. PII is masked in results by default, and users can delete individual records or clear local history.

## Validation

The repository contains a deterministic data-preparation manifest, fixed train/validation/test splits, model-selection report, evaluation report, ROC/PR outputs, ONNX equivalence report, adversarial functional suite, runtime report, package manifest, and build hash. The verified state has 77 passing backend tests plus passing frontend lint, strict TypeScript, production build, and dependency audits.

## Impact and differentiation matrix

| Dimension | Common single-channel or cloud workflow | SnapShield AI | User impact |
|---|---|---|---|
| Input coverage | Text or URL handled separately | Messages, URLs, screenshots, OCR text, and QR payloads feed one pipeline | Less manual correlation |
| Data boundary | Evidence may be uploaded remotely | Local analysis; raw source excluded from persistent history | Reduced exposure of sensitive evidence |
| Explainability | Label or opaque score | Named indicators, contributions, explanation, and action | Faster, more defensible decisions |
| URL safety | Reputation lookup or navigation may be required | Structural parsing without opening the destination | No contact with the suspicious site |
| Model strategy | Large general model or single classifier | Compact ONNX model plus independent deterministic engines | Predictable, inspectable local behavior |
| Hardware claims | Accelerator inferred from platform marketing | Actual provider detected; QNN must pass a strict verification gate | Honest and reproducible acceleration claims |
| Resilience | Cloud/network dependency | Local pipeline with CPU fallback | Useful offline and during connectivity loss |

## Repository

Use the public repository URL after confirming that it exposes no secret, private path, personal data, or internal-only artifact. The canonical technical facts are in `SUBMISSION_FACTS.md`.

## Demo video description

The demo shows a benign control, a synthetic bank-themed phishing message, a multimodal screenshot containing OCR and QR evidence, local PII redaction, sanitized incident history, and the Runtime page’s honest provider report. All malicious-looking inputs are inert synthetic examples.
