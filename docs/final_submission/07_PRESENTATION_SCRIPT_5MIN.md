# Presentation script - approximately five minutes

## Slide 1 - Hero (0:00-0:30)

"This is SnapShield AI, a private, on-device multimodal cyber-defense copilot designed for Snapdragon PCs. Its purpose is simple: your data should not need to leave your device to protect your device. SnapShield inspects suspicious messages, links, screenshots, QR codes, and sensitive information locally, then returns risk, evidence, and a practical action."

Transition: "The reason local processing matters starts with the data security tools have to inspect."

## Slide 2 - Problem (0:30-1:05)

"A suspicious message may contain a private conversation, banking context, a phone number, an email address, or authentication instructions. Screenshots hide text from ordinary filters, and QR codes hide their destination behind an image. Remote AI can be useful, but sending this material across another trust boundary creates privacy, connectivity, and governance concerns. Users need help before they know whether the content itself can be trusted."

Transition: "SnapShield keeps that first line of analysis on the PC."

## Slide 3 - Solution (1:05-1:40)

"The interaction is intentionally direct. Give SnapShield a message, URL, screenshot, or QR image. It produces four things: a bounded risk score, a plain-language reason, the exact evidence behind the result, and a recommended action. Submitted URLs are parsed but never opened. Core analysis uses no cloud AI, and incidents store only a hash and sanitized derived metadata rather than the original content."

Transition: "Underneath that simple result is a set of specialized engines."

## Slide 4 - How it works (1:40-2:25)

"Images first pass byte, format, and decoded-pixel validation. RapidOCR extracts text locally, and OpenCV decodes QR payloads. Text then enters a lightweight TF-IDF classifier running through ONNX Runtime. In parallel, deterministic engines inspect social-engineering language, Unicode obfuscation, URL structure, controlled brand-domain mismatches, and PII.

"Every engine emits structured evidence. A transparent policy fuses those findings, discounts weak isolated signals, bounds the score, and builds the explanation and next actions. The learned classifier supports the decision; it does not override stronger URL, credential, QR, or brand evidence."

Transition: "That architecture is backed by a reproducible evaluation."

## Slide 5 - Real results (2:25-3:15)

"The primary dataset is the UCI SMS Spam Collection under CC BY 4.0. Deduplication happened before splitting: 5,574 original messages became 5,105 retained records. We used 3,573 for training, 766 for validation, and one untouched test split of 766.

"On that SMS test set, the final model achieved 98.17 percent accuracy, 95.37 percent macro F1, 97.50 percent spam precision, and 86.67 percent spam recall. The 13.33 percent false-negative rate is important, so we report it and keep the model as only one signal. The 41-kilobyte FP32 ONNX graph matched the reference class on all 766 test samples. The backend now has 77 passing tests, and the median full text pipeline is 5.09 milliseconds on this development CPU."

Transition: "The provider boundary is also where Snapdragon becomes relevant."

## Slide 6 - Why Snapdragon (3:15-3:55)

"Today, the verified provider is CPUExecutionProvider on an Intel AMD64 development machine. I am not claiming a Snapdragon NPU result. What is complete is the deployment architecture: the FP32 ONNX model, an 11.7-kilobyte QDQ candidate, provider discovery, a QNN HTP execution path, CPU-fallback-disabled validation, and an exact model filename and SHA-256 gate.

"That means the application logic is separated from the inference provider and is ready for a named Snapdragon hardware qualification run. No speed or battery number will be claimed until that run exists."

Transition: "The flagship product experience shows why that local path matters."

## Slide 7 - Product and impact (3:55-4:30)

"A single phishing screenshot can contain visible social engineering, a suspicious link, personal data, and a QR destination. SnapShield extracts and analyzes those elements together, then explains which ones drove the score. This can support students and families checking unexpected requests, professionals triaging messages, small businesses reviewing payment lures, and enterprises exploring privacy-first local assistance. It complements broader endpoint and reputation tools; it does not replace them."

Transition: "The project closes on a clear, technically honest proposition."

## Slide 8 - Closing (4:30-4:55)

"SnapShield combines real licensed data, a verified ONNX model, working local OCR and QR analysis, transparent cybersecurity evidence, and a credible QNN deployment path. The current build proves the product on CPU; the next validation step is named Snapdragon hardware. SnapShield AI: private AI, local security, designed for Snapdragon."

## Delivery notes

- Pause briefly after `86.67 percent recall`; do not bury it.
- Point to `CPU verified` before the QNN target branch.
- Keep the phrase `on that SMS test set` attached to model metrics.
- If time slips, shorten slides 2 and 7; never rush the Snapdragon status disclosure.
