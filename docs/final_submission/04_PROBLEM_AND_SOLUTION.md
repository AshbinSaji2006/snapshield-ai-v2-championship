# Problem and solution

## Competition problem statement

Phishing and scams are difficult because they target human judgment, not just software vulnerabilities. A convincing message can combine urgency, a familiar brand, a plausible link, and a request that looks routine. Screenshots hide important text from ordinary message filters, while QR codes move the destination behind an image and encourage users to switch devices or contexts before checking it.

AI can help recognize patterns across these inputs, but the material being inspected is often unusually sensitive: private conversations, banking context, email addresses, phone numbers, authentication instructions, and confidential business information. Requiring that content to travel to a remote AI service introduces an additional privacy, connectivity, and governance boundary precisely when the user is already uncertain about whom to trust.

The challenge is therefore broader than classifying spam. Users need a fast, understandable way to inspect messages, URLs, screenshots, QR codes, and exposed sensitive data locally. The result must explain the evidence and recommend a safe action without pretending that any classifier can guarantee safety.

## Solution in simple language

Give SnapShield a suspicious message, link, screenshot, or QR image. It analyzes the content locally and returns four things:

1. **Risk** - a bounded score and severity.
2. **Reason** - a plain-language explanation.
3. **Evidence** - the specific signals that affected the result.
4. **Action** - practical next steps, such as using an official app or verifying the sender independently.

SnapShield never needs to open the submitted link or send the content to cloud AI.

## Solution in technical language

Validated input enters a local FastAPI orchestration layer. Images pass through defensive Pillow validation, RapidOCR, and OpenCV QR decoding. Extracted text and QR payloads join direct message/URL inputs and fan out to a TF-IDF/ONNX classifier, social-engineering rules, Unicode-obfuscation checks, structural URL forensics, controlled brand-domain mismatch detection, and PII detection/redaction.

Each engine emits structured evidence with a stable ID, description, contribution, and sanitized details. A deterministic risk-fusion policy applies corroboration adjustments, caps the score, selects a severity band, and generates an evidence-based explanation and recommended actions. Optional incidents persist only a SHA-256 input hash and sanitized derived metadata in local SQLite.

ONNX Runtime isolates application logic from the execution provider. CPUExecutionProvider is verified today. A QDQ model, QNN HTP path, CPU-fallback-disabled validation session, and exact artifact-hash gate are implemented for future Snapdragon hardware validation.

## Innovation

SnapShield does not depend on one LLM or one classifier. Its innovation is the local composition of learned and deterministic security components across text and images, with the same evidence model carrying OCR text and QR payloads through URL, brand, PII, and risk analysis. This produces repeatable, inspectable output while preserving an offline privacy boundary.

## Vision

SnapShield can evolve into a continuous, user-consented security copilot for Snapdragon PCs: inspecting risky content close to where it appears, using efficient local acceleration, and escalating uncertainty without requiring private material to leave the machine.
