# Eight-slide presentation content

Design direction: dark charcoal background, mint verified-state accent, amber target-state accent, coral threat accent. Use one message per slide, large type, and no paragraph blocks. Screenshots must come from the actual production build.

## Slide 1 - Hero

**SnapShield AI**

Private On-Device Multimodal Cyber Defense for Snapdragon PCs

**Your data never needs to leave your device to protect your device.**

Visual: full-width actual Overview screenshot with the Local processing chip and exact runtime label visible.

Footer: `CPU verified today | Snapdragon QNN path ready for hardware validation`

## Slide 2 - Problem

**Security AI has a privacy problem.**

Large visual tokens:

`Private message` `Banking screenshot` `QR code` `Suspicious URL`

Arrow to: `Remote processing boundary`

Single line: **Users should not have to disclose private content just to ask whether it is dangerous.**

Visual: privacy comparison from `05_ARCHITECTURE.md`.

## Slide 3 - Solution

**Risk. Reason. Evidence. Action. All local.**

`Message + URL + Screenshot + QR` -> **SnapShield AI** -> `Score + Evidence + Recommendation`

Three proof points:

- No cloud AI required
- Submitted URLs are never opened
- Raw source is not stored in incidents

Visual: actual phishing result card, lightly cropped but retaining provider and severity.

## Slide 4 - How it works

**Multiple specialized signals. One explainable assessment.**

Use the presentation architecture diagram. Highlight only:

- TF-IDF + ONNX classifier
- RapidOCR + OpenCV QR
- URL + brand + PII + security rules
- Risk fusion + explanation
- Sanitized local incidents

Bottom runtime strip:

`ONNX Runtime` -> `CPUExecutionProvider - verified`

Dashed amber: `QNN / Snapdragon NPU - hardware validation pending`

## Slide 5 - Real results

**Measured, reproducible, and scoped.**

Hero numbers:

- **5,105** retained deduplicated UCI SMS messages
- **98.17%** held-out accuracy
- **95.37%** macro F1
- **86.67%** spam recall
- **0.30%** false-positive rate
- **100%** ONNX/reference class agreement
- **77** backend tests passed
- **5.09 ms** median full text pipeline on the development CPU

Required scope label: **Classifier metrics: untouched 766-message UCI SMS test split. Latency: Intel/AMD64 CPUExecutionProvider. Not universal phishing or Snapdragon performance.**

Visual: confusion matrix plot plus a small ONNX artifact card (`41,447 bytes`, opset 17).

## Slide 6 - Why Snapdragon

**Built around local inference. Designed for Snapdragon acceleration.**

Two columns:

**Verified today**

- FP32 ONNX equivalent to reference
- CPUExecutionProvider
- Provider detection and fallbacks
- Local OCR, QR, and multimodal fusion

**Target hardware path**

- QDQ candidate
- QNN HTP execution code
- CPU-fallback-disabled validation
- Exact model-hash gate
- Native ARM64 validation pending

Closing line: **No NPU speed, power, or battery claim without a real Snapdragon run.**

## Slide 7 - Product demo and impact

**One screenshot. Multiple layers of defense.**

`Image` -> `OCR` -> `Text + URL` -> `QR` -> `PII` -> `Risk + Action`

Visual: actual multimodal result with OCR and QR details visible.

Use cases: `Students` `Families` `Professionals` `Small businesses` `Enterprises`

Impact line: **Fast, understandable triage for private content - with offline core operation.**

## Slide 8 - Closing

**SnapShield AI**

Private AI. Local security. Designed for Snapdragon.

**Your data never needs to leave your device to protect your device.**

Three closing proofs:

`Real data` `Real ONNX` `Real multimodal pipeline`

Small honesty line: `Current provider: CPUExecutionProvider | QNN hardware validation pending`
