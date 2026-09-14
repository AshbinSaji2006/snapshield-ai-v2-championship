# Final Presenter Script

Target delivery: **4:55**. Speak naturally; the timing includes short pauses for pointing.

## Slide 1 — SnapShield AI

**TIME** 0:00–0:30

**WHAT TO SAY**

"Suspicious security content can expose the very data people are trying to protect. This is SnapShield AI: private, on-device, multimodal cyber defense for Snapdragon-powered PCs. It analyzes suspicious messages, URLs, screenshots, and QR codes locally, then returns a risk score, the evidence behind it, and a safe next action. The promise is simple: your data never needs to leave your device to protect your device."

**WHAT TO POINT AT**

The real dashboard, **LOCAL PROCESSING**, and **CPUExecutionProvider**.

**TRANSITION**

"That local boundary matters because the material we ask security tools to inspect is often private."

## Slide 2 — Security AI Has a Privacy Problem

**TIME** 0:30–1:05

**WHAT TO SAY**

"A suspicious message can contain banking context. A screenshot can expose personal information. A QR code can conceal a destination. Cloud-dependent analysis may require that content to cross an additional network and service boundary. SnapShield keeps its core analysis on the PC. That reduces routine data exposure without pretending endpoint security no longer matters."

**WHAT TO POINT AT**

Trace the left flow from private content through the internet to cloud AI, then contrast it with the shorter local flow.

**TRANSITION**

"We built one local copilot for all four of those threat surfaces."

## Slide 3 — One Local Security Copilot

**TIME** 1:05–1:40

**WHAT TO SAY**

"SnapShield is not simply a spam classifier. The compact text model is one signal. URL forensics, social-engineering indicators, OCR, QR decoding, brand and domain checks, PII analysis, and deterministic security rules contribute independent evidence. The result is a bounded evidence-weighted risk score—not a probability—with an explanation and a practical recommendation."

**WHAT TO POINT AT**

Move from **MESSAGE / URL / SCREENSHOT / QR** to **RISK / EVIDENCE / ACTION**, then point to the real critical analysis.

**TRANSITION**

"Here is how those signals become one explainable decision."

## Slide 4 — Local-First Architecture

**TIME** 1:40–2:25

**WHAT TO SAY**

"Inputs enter specialized local engines. Visible text goes through OCR and the text model; URLs are structurally inspected but never opened; QR payloads are decoded locally; PII can be identified and redacted; and security rules recognize persuasion and evasion patterns. Risk fusion combines the evidence. The application returns an explanation and recommendation, while incident history stores only a hash and sanitized derived metadata. The runtime layer reports the provider it actually selected: CPU is verified here; the QNN and Snapdragon NPU path still needs compatible-device validation."

**WHAT TO POINT AT**

Trace left to right, then finish on the bottom provider rail and the amber pending box.

**TRANSITION**

"That claim discipline also applies to every engineering number."

## Slide 5 — Real Engineering Results

**TIME** 2:25–3:15

**WHAT TO SAY**

"The model evaluation uses 5,105 retained, deduplicated messages from the UCI SMS Spam Collection, with a fixed 766-message held-out test split. On that test set, accuracy is 98.17 percent, macro F1 is 95.37 percent, spam recall is 86.67 percent, and the false-positive rate is 0.30 percent. The 13.33 percent false-negative rate is a known limitation. The FP32 ONNX export has 100 percent class agreement across all 766 held-out samples. Seventy-seven backend tests pass. The recorded median full text pipeline is 5.09 milliseconds on the current development CPU—not Snapdragon performance."

**WHAT TO POINT AT**

Point first to the dataset size and footnote, then the quality metrics, ONNX agreement, tests, and CPU timing.

**TRANSITION**

"The strongest proof that this is more than text classification is the screenshot pipeline."

## Slide 6 — A Screenshot Becomes Security Evidence

**TIME** 3:15–3:55

**WHAT TO SAY**

"This is a real application result from a synthetic, inert phishing screenshot. Local OCR recovers the visible message. The QR decoder extracts its payload without navigating to it. URL structure, social-engineering language, PII, and brand-domain evidence are correlated by the same risk-fusion layer. One screenshot becomes inspectable evidence and an explainable action, while the submitted image stays on the device."

**WHAT TO POINT AT**

Point to the OCR text, QR payload, **NEVER OPENED** label, critical score, and evidence trail.

**TRANSITION**

"That local architecture maps naturally to Snapdragon PCs, but readiness and proof must stay separate."

## Slide 7 — Why Snapdragon

**TIME** 3:55–4:30

**WHAT TO SAY**

"Today, ONNX Runtime, CPUExecutionProvider, and local inference are verified. The code also implements provider abstraction, a QNN execution path, an exact-artifact validation gate, and a QDQ candidate. The next hardware step is a real Snapdragon NPU validation run. Until that happens, we make no NPU latency, power, or battery claim. The architecture is Snapdragon-ready; hardware validation is pending."

**WHAT TO POINT AT**

Move across **VERIFIED TODAY**, **IMPLEMENTED**, and **NEXT HARDWARE STEP**. Pause on the amber qualification.

**TRANSITION**

"The product is useful now, and the deployment path is explicit."

## Slide 8 — Private AI. Local Security.

**TIME** 4:30–4:55

**WHAT TO SAY**

"SnapShield AI brings private AI and local security together in a working multimodal product. It is verified on CPU today and designed for Snapdragon. Our vision is a future where checking whether something is dangerous does not require giving it away first. Our next measurable milestone is verified QNN execution on compatible Snapdragon hardware."

**WHAT TO POINT AT**

The real dashboard, the verified runtime line, and **QNN hardware validation pending**.

**TRANSITION**

End and invite questions.
