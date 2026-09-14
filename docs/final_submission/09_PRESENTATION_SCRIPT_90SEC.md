# Emergency 90-second pitch

"Security analysis often starts with highly private content: messages, banking screenshots, links, QR codes, and authentication information. SnapShield AI is a multimodal cyber-defense copilot that keeps its core analysis on the PC.

"A user submits a message, URL, or image and receives risk, reason, evidence, and action. RapidOCR extracts screenshot text locally, OpenCV decodes QR payloads, and a compact ONNX classifier works alongside URL forensics, social-engineering rules, brand-domain checks, Unicode-evasion detection, and PII redaction. The classifier supports the verdict; transparent multi-signal fusion makes the final assessment.

"The model was trained with 5,105 deduplicated UCI SMS messages. On an untouched 766-message SMS test split, it achieved 98.17 percent accuracy, 95.37 percent macro F1, and 86.67 percent spam recall. Its 41-kilobyte ONNX export matched the reference class on all 766 samples. The backend has 77 passing tests, and the median full text pipeline was 5.09 milliseconds on the development CPU.

"Today, CPUExecutionProvider is verified. Snapdragon NPU execution is not. The QDQ model, QNN path, exact hash gate, fallback, and validation reporting are implemented for target hardware qualification. SnapShield delivers private AI, local security, and a credible path to Snapdragon acceleration - without inventing an NPU result."
