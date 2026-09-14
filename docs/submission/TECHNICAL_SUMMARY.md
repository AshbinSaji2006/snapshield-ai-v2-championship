# Technical summary

React 19/TypeScript 7 provides a responsive presentation console. FastAPI validates loopback requests and orchestrates ONNX text inference, deterministic URL/text/Unicode/brand checks, PII redaction, RapidOCR, and OpenCV QR. Expert-authored contributions produce a bounded evidence score; SQLite stores only hashes and sanitized derived metadata.

The model uses 10,264 word TF-IDF features and logistic regression trained on 4,339 deduplicated UCI train+validation messages. The untouched 766-message test produced 98.17% accuracy, 97.50% spam precision, 86.67% recall, 91.76% F1, 95.37% macro F1, 0.30% FPR, and 13.33% FNR. ONNX Runtime is primary; all 766 classes matched scikit-learn. This machine selected CPU. QNN/HTP validation is pending target Snapdragon hardware.

The final gate includes 77 backend tests, frontend lint/type/build/audit, an 18-case adversarial regression suite, component-separated benchmarks, and a smoke-tested unsigned Windows package.
