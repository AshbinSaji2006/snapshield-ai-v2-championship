# Final Scorecard and Multi-Role Review

## Executive score

**Current submission readiness: 9.3/10.** The real screenshots, rendered visuals, eight-slide deck, synchronized PDF, scripts, and evidence discipline are complete. The score remains capped because the real demo recording, public repository publication, presentation-laptop check, and compatible-device QNN evidence still require human or hardware completion.

| Area | Score / 10 | Basis |
|---|---:|---|
| Problem relevance | 9.2 | Clear, current privacy/security problem across several content types |
| Product completeness | 9.1 | Working UI, local pipeline, explanations, incidents, runtime truth, package |
| Technical design | 9.1 | Layered engines, ONNX deployment, reproducible artifacts, clear boundaries |
| Evaluation rigor | 8.7 | Strong leakage controls and exact reports; narrow/older text corpus limits scope |
| Privacy and security | 9.4 | Local-first, no URL navigation, redaction, minimized persistence; endpoint trust remains |
| Snapdragon alignment | 7.7 | Real QNN-ready implementation, but no compatible-device execution evidence |
| Explainability and demo | 9.3 | Evidence contributions, safe built-in samples, presentation and recovery flows |
| Differentiation | 8.7 | Cohesive local multimodal workflow; component techniques are individually established |
| Claim credibility | 9.8 | Unverified NPU and dataset scope are disclosed consistently and visibly |
| Submission operations | 9.0 | Judge-facing release complete; video, public URL, presentation-laptop check, and portal upload remain |

## Review 1 — Competition judge

**Likely verdict:** A polished, credible local-AI security prototype with a memorable privacy promise.

Top concerns:

1. **Is Snapdragon use real?** Addressed with an exact implemented-versus-verified table and an honest Runtime screen; hardware proof remains open.
2. **Is the 98.17% figure overstated?** Addressed by naming the retained UCI SMS test split, confusion matrix, and recall every time.
3. **What is demonstrably multimodal?** Addressed by the bundled OCR-plus-QR flow and a real 1920 × 1080 application capture.
4. **Is it more than a classifier demo?** Addressed by URL, social-engineering, PII, brand, OCR, QR, fusion, incidents, and runtime evidence.
5. **Will the live demo survive?** Addressed through built-in inert inputs, a two-minute exact flow, and an offline recovery ladder.

## Review 2 — Cybersecurity expert

**Likely verdict:** Strongly scoped decision support, provided it is not presented as endpoint protection.

Top concerns:

1. **False negatives create false reassurance.** Explicit 12/90 missed spam count and “low risk is not proof of safety” boundary.
2. **No live reputation or destination analysis.** Documented as a deliberate privacy/safety tradeoff.
3. **Finite rule and language coverage.** Documented limitation with broader and multilingual evaluation roadmap.
4. **Compromised-host threat.** Local processing is not presented as protection from a privileged local attacker.
5. **Unsigned distribution.** `NotSigned` is disclosed; signing and supply-chain hardening are first-class roadmap items.

## Review 3 — ML engineer

**Likely verdict:** Appropriately simple, unusually reproducible deployment for a competition project.

Top concerns:

1. **Old and narrow training corpus.** Treated as a baseline component, not product-level proof.
2. **Class imbalance.** Precision, recall, F1, FPR, FNR, ROC AUC, PR AUC, and exact counts are reported.
3. **Leakage.** Exact and normalized near-duplicate removal occurs before a fixed stratified split.
4. **Quantization drift.** FP32 stays primary; QDQ deviation and calibration source are disclosed.
5. **End-to-end metrics missing.** The distinction between classifier, functional, and product evaluation is explicit.

## Review 4 — Snapdragon/edge-AI reviewer

**Likely verdict:** Credible accelerator-ready engineering, but not yet a completed Snapdragon NPU validation story.

Top concerns:

1. **No physical Snapdragon run.** Clearly disclosed and made the first roadmap milestone.
2. **Silent CPU fallback.** Strict verification, provider reporting, and model-hash gates are documented.
3. **Value of NPU for a tiny linear graph.** No speed claim; measurement will decide which pipeline stages benefit.
4. **No ARM64 package.** Current package is explicitly AMD64; ARM64 packaging is pending.
5. **No power/thermal evidence.** No efficiency statement is made without instrumentation.

## Review 5 — Product and presentation reviewer

**Likely verdict:** Strong story and UI; submission quality now depends on disciplined visual execution.

Top concerns:

1. **Too much technical detail early.** The scripts lead with the user problem and reveal metrics after the product value.
2. **Crowded slides.** Eight-slide content gives each slide one job and one primary visual.
3. **Demo time risk.** The video runbook is timed to 3:35, with explicit cut points and screenshot fallbacks.
4. **Inconsistent terminology.** The canonical title, subtitle, tagline, facts, and claims are centralized.
5. **Missing final media.** Only the real screen recording remains; screenshots, deck, PDF, scripts, and fallback evidence are complete.

## What would raise the score

- Verified QNN/HTP execution and a reproducible compatible-device report: **+0.4 to +0.6**.
- A clean, timed real-application demo video and successful presentation-laptop rehearsal: **+0.1 to +0.2**.
- A broader modern product-level evaluation with confidence intervals and subgroup analysis: **+0.3 to +0.5**.
- Signed ARM64 distribution and external security review: **+0.2 to +0.4**.

These improvements are not additive guarantees. Competition scoring depends on the rubric and judge priorities.

## Go/no-go assessment

**Go for submission after the real demo video, public repository URL, presentation-laptop check, and portal preview are completed.** Do not delay submission to manufacture NPU evidence. A truthful CPU demo with a precise compatible-device plan is stronger than an unsupported acceleration claim.
