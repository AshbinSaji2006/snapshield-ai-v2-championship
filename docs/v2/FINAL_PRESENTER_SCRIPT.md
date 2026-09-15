# SnapShield AI v2 — five-minute presenter script

## Slide 1 — 0:00–0:30

**What to say:** “SnapShield AI is a private, local-first cyber-defense copilot for messages, URLs, screenshots, and QR codes. Its promise is simple: your data never needs to leave your device to protect your device. This is the real v2 application, running locally through ONNX Runtime on CPUExecutionProvider.”

**Point at:** Local processing, Fast Guard, Deep Guard, and the current provider.

**Transition:** “That local boundary matters because suspicious content can itself be sensitive.”

## Slide 2 — 0:30–1:00

**What to say:** “A suspicious message may contain banking context, phone numbers, screenshots, or authentication instructions. Cloud-dependent analysis may require remote processing, adding another trust boundary. SnapShield’s core flow performs analysis on the PC; endpoint security still matters, but the content does not need a cloud AI round trip.”

**Point at:** The additional cloud boundary, then the shorter local flow.

**Transition:** “Inside that boundary, SnapShield covers more than text classification.”

## Slide 3 — 1:00–1:35

**What to say:** “One interface accepts a message, a URL, a screenshot, or a QR code. It returns an ordinal risk score, the evidence behind it, and a practical action. URLs are parsed but never visited. Incident history excludes raw source content.”

**Point at:** Risk, Evidence, Action and the real phishing result.

**Transition:** “The architecture turns each input into correlated evidence.”

## Slide 4 — 1:35–2:15

**What to say:** “The local pipeline combines a calibrated Fast Guard, an adaptive router, and a BERT Tiny Deep Guard with URL forensics, OCR, QR decoding, PII analysis, brand/domain checks, and India-focused security rules. A Threat Evidence Graph preserves relationships before bounded risk fusion produces an explanation and recommendation. CPU execution is verified. The QNN/Snapdragon NPU route and exact-artifact gate are implemented, but compatible-hardware validation is pending.”

**Point at:** Adaptive ML, graph/fusion, then the solid CPU box and dashed QNN box.

**Transition:** “We evaluated each layer with named, reproducible evidence.”

## Slide 5 — 2:15–3:10

**What to say:** “The base corpus contains 5,105 deduplicated UCI messages. On its untouched 766-message test, Deep Guard reached 94.44 percent positive recall. On a separately sourced, strictly UCI-deduplicated 521-message 2022 Mendeley holdout, it reached 98.04 percent recall. Adaptive routing held UCI recall while reducing false positives to 0.30 percent and escalating 33.68 percent of UCI messages. We also have 100 backend tests, 20 of 20 curated robustness checks, and exact FP32-to-QDQ class agreement on both holdouts. These are dataset-specific SMS results, not universal phishing accuracy. The 28.69 millisecond pipeline number is from this development CPU, not Snapdragon.”

**Point at:** Dataset labels first, then recall, FPR, tests, and timing.

**Transition:** “The clearest proof that this is more than a spam model is the screenshot path.”

## Slide 6 — 3:10–3:50

**What to say:** “This synthetic, inert bank alert is a real application run. SnapShield defensively decodes the image, extracts visible text with RapidOCR, decodes the QR locally, identifies the destination without opening it, correlates brand and domain evidence, and exposes the result as a threat graph and evidence trail.”

**Point at:** OCR text, decoded QR payload, destination, then graph connections.

**Transition:** “That workload is exactly why the Snapdragon deployment path is relevant.”

## Slide 7 — 3:50–4:30

**What to say:** “Security AI belongs close to private data. Today we verify ONNX Runtime, CPUExecutionProvider, and local inference. We implemented provider abstraction, a strict QNN path, an exact-artifact gate, a QDQ candidate, and Qualcomm AI Hub automation. The next hardware step is measured Snapdragon NPU validation. We make no NPU latency, power, or battery claim without that run.”

**Point at:** Verified, Implemented, Next; finish on ‘hardware validation pending’.

**Transition:** “So the value is already real, and the remaining hardware claim is precisely bounded.”

## Slide 8 — 4:30–5:00

**What to say:** “SnapShield AI combines adaptive local ML, multimodal evidence, privacy-minimal history, and explainable action in a working Windows product. It is private AI, local security, and designed for Snapdragon. Checking whether something is dangerous should not require giving it away first.”

**Point at:** Real application and current verified provider.

**Transition:** “Thank you—I’m ready for your questions.”
