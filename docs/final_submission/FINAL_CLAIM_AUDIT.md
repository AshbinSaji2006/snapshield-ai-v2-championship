# Final Claim and Submission QA

Audit date: **2026-09-13**

Result: **PASS for all generated submission-facing artifacts.** Remaining work is external/human: real video recording, repository publication, presentation-laptop rehearsal, portal upload, code signing/native ARM64 if available, and compatible-device QNN validation.

## Scope checked

- `README.md`, `SUBMISSION_FACTS.md`, model/test/benchmark/Snapdragon documentation.
- All Markdown and text files in `docs/final_submission/` and `release/final_submission/`.
- Extracted text from all 8 PPTX slides and page count/dimensions from the PowerPoint-exported PDF.
- All eight real screenshots, architecture/privacy graphics, presenter script, demo narration, recording guide, form answers, handoff, and release manifests.
- Package identity and Authenticode state.

## Canonical facts

| Claim | Audited value and required context | Status |
|---|---|---|
| Dataset | UCI SMS Spam Collection, DOI `10.24432/C5CC84`, CC BY 4.0 | Pass |
| Rows | 5,574 original; 5,105 retained; 3,573 train; 766 validation; 766 test | Pass |
| Text classifier | 98.17% accuracy, 97.50% precision, 86.67% recall, 91.76% spam F1, 95.37% macro F1, 98.13% weighted F1 | Pass—always scoped to the fixed retained UCI SMS split |
| Error/AUC metrics | 0.30% FPR, 13.33% FNR, 0.9928 ROC-AUC, 0.9722 PR-AUC | Pass |
| ONNX | 100% FP32 class agreement across 766 held-out samples | Pass |
| Tests | 77 backend tests passed on 2026-09-13 | Pass |
| Recorded CPU timing | 5.09 ms median full text pipeline; 1,863.35 ms median full multimodal pipeline | Pass—not Snapdragon results |
| Current runtime | `CPUExecutionProvider` | Pass |
| Hardware status | QNN execution path implemented; Snapdragon NPU hardware validation pending | Pass |
| Windows package | AMD64, unsigned, 372.28 MiB, 1,363 files | Pass |

The Runtime screenshot's **5.88 ms median / 11.15 ms p95 / 25 iterations** is explicitly recorded in `SUBMISSION_FACTS.md` as a point-in-time interactive UI run. It does not replace the canonical 200-iteration benchmark.

## Language audit

- No affirmative claim says **Powered by Snapdragon NPU**, **Running on Snapdragon NPU**, **NPU accelerated**, **Snapdragon validated**, **QNN validated**, or **Snapdragon optimized**.
- Matches for those phrases occur only inside explicit **do not say**, **disallowed wording**, or future validation instructions.
- No affirmative claim describes 98.17% as universal or production phishing detection accuracy.
- The text classifier is consistently presented as one signal in the multimodal security pipeline.
- The fused score is described as bounded/evidence-weighted, not a calibrated probability.
- CPU verification and QNN/Snapdragon hardware readiness are visually and verbally separated.

## Presentation export validation

- PPTX: 8 slides, 16:9 (`12191999 × 6858000` EMU).
- PDF: 8 pages, 16:9 media box (`960 × 540` points), exported from the final PPTX through Microsoft PowerPoint.
- 1080p slide proofs were visually reviewed for clipping, overflow, duplicated labels, image crops, contrast, and room readability.
- Metrics footnote names the UCI SMS test set and rejects universal phishing-accuracy interpretation.
- Slides 4, 7, and 8 clearly show CPU verified versus QNN/Snapdragon NPU hardware validation pending.

## Screenshot validation

- Eight uniquely named PNGs exist at exactly 1920 × 1080.
- The capture manifest identifies `http://127.0.0.1:8765`, `CPUExecutionProvider`, `snapdragon_npu_verified: false`, and real-application capture.
- Captures show settled UI states with no browser chrome, debug console, cursor obstruction, broken icon, loading state, or placeholder result.
- The image/QR samples are synthetic and inert. Decoded URLs are displayed and inspected, never opened.

## Multi-role review

- **Qualcomm/edge engineer:** provider evidence is honest; QNN path and next validation gate are concrete; no unmeasured NPU benefit is claimed.
- **ML reviewer:** dataset, split, duplicate handling, class metrics, false negatives, ONNX agreement, and scope limitations are visible.
- **Cybersecurity judge:** product is framed as decision support, with structural URL analysis, safe decoding, evidence, and explicit residual risk.
- **Product judge:** the problem is clear within the opening slide, and the multimodal screenshot differentiates the product from a single classifier.
- **Presentation judge:** eight slides have one job each, use real product imagery, and keep key claims readable at 1080p.

## Engineering freeze confirmation

No dataset, model, ONNX artifact, risk scoring, security rule, benchmark methodology, API contract, or backend architecture changed. The only production changes were narrow submission-blocking corrections: displaying already-returned OCR/QR evidence in the result UI and allowing the application's own required loopback origins so packaged module assets render.
