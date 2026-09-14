# Roadmap

The roadmap preserves the current architecture and prioritizes evidence before expansion.

## Phase 1 — Hardware validation

**Goal:** convert Snapdragon readiness into a verified device result.

- Produce and smoke-test a complete Windows ARM64 package.
- Run the strict QNN/HTP provider gate on a compatible Snapdragon PC.
- Capture provider, node-assignment, artifact-hash, prediction-equivalence, and environment reports.
- Benchmark fixed text and multimodal workloads with warm-up, median, P95, memory, and sustained runs.
- Measure power or thermals only with reliable instrumentation and publish the method.
- Sign the Windows package and document provenance.

Exit criterion: an independently reviewable device report supports every Snapdragon execution claim.

## Phase 2 — Evaluation depth

**Goal:** measure the complete product against current threat distributions.

- Build licensed, provenance-tracked corpora for modern SMS, email, collaboration messages, screenshots, QR lures, and benign hard negatives.
- Add multilingual and code-mixed evaluation.
- Define end-to-end labels for OCR, QR extraction, URL indicators, PII, brand mismatch, fused severity, and recommended action.
- Perform threshold calibration, subgroup analysis, temporal holdouts, confidence intervals, and false-negative review.
- Add image-corruption and adversarial-text robustness matrices.

Exit criterion: product-level metrics are reported separately from classifier metrics with auditable sampling and leakage controls.

## Phase 3 — Product hardening

**Goal:** make local-first protection deployable beyond a competition prototype.

- Add signed updates, model manifest verification, rollback, and secure configuration storage.
- Threat-model the loopback API, installer, local database, and artifact supply chain.
- Add enterprise policy controls for retention and redaction without retaining raw source by default.
- Improve accessibility, localization, telemetry-free diagnostics, and recovery behavior.
- Conduct external penetration testing and privacy review.

Exit criterion: the build meets a documented release checklist and security review threshold.

## Phase 4 — Carefully scoped integrations

**Goal:** reduce user effort without expanding the data boundary silently.

- Evaluate explicit-share extensions for browsers, mail clients, and messaging applications.
- Keep content local unless a user or administrator deliberately enables an external service.
- Support export of sanitized evidence bundles for incident-response teams.
- Explore organization-specific, locally deployed policy packs and brand/domain mappings.

Exit criterion: each integration has transparent permissions, consent, retention, and rollback behavior.

## Research directions

- Compare compact transformer, character-level, and linear models under equal memory, latency, and energy budgets.
- Investigate calibrated uncertainty and abstention for ambiguous cases.
- Evaluate NPU-suitable OCR and multi-stage routing after device measurement.
- Study concept-drift detection without uploading private user content.
- Test privacy-preserving local personalization with strict rollback and evaluation gates.

## Deliberate non-goals until evidence exists

- Claiming universal phishing detection.
- Automatic blocking or account remediation.
- Replacing endpoint protection or secure email gateways.
- Advertising Snapdragon NPU speed, power, or battery gains before device measurement.
- Adding a large model only for novelty; any new model must beat the current pipeline under explicit quality and resource constraints.
