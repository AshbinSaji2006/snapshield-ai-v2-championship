# SnapShield AI v2 — rejected or deferred features

| Feature/approach | Status | Reason |
|---|---|---|
| Adaptive router v2.1 | REJECTED | Escalated only about 7–8% and reached 76.96% external recall, far below Deep Guard’s 98.04%. The report is preserved. |
| Additional transformer tournament candidates | REJECTED | Three credible candidates established an edge Pareto winner; more training would add cost without a clear decision need. |
| Vision transformer/logo model | REJECTED FOR THIS RELEASE | OCR + QR + brand/domain correlation already produce demonstrable multimodal security evidence; no measured incremental value justified another model. |
| Local generative explanation model | REJECTED FOR THIS RELEASE | Would add size, latency, non-determinism, and a new claim surface. Explanations remain evidence-derived. |
| Silent/background clipboard capture | REJECTED | Violates privacy and demo transparency. Live Shield is explicit opt-in with a visible state. |
| Automatic URL navigation/reputation lookup | REJECTED | Would contact suspicious infrastructure and weaken the offline/privacy boundary. |
| QDQ as default runtime on this AMD64 host | DEFERRED | Numerical agreement is verified, but QNN assignment/performance is not; FP32 CPU remains the honest deployed path. |
| Claimed Snapdragon performance estimates | REJECTED | No compatible-device measurement exists. |
| Cross-compiling an AMD64 package and labeling it ARM64 | REJECTED | PyInstaller is not a cross-compiler; native ARM64 remains a documented external build step. |
