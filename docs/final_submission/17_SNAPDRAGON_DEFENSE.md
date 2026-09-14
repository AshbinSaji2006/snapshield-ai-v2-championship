# Snapdragon and QNN Defense

## The exact answer

“SnapShield is **designed for Snapdragon PCs**, and its QNN execution path is implemented, but this development machine is AMD64 and does not expose the QNN provider. The verified build therefore reports `CPUExecutionProvider`. We have an NPU-prepared QDQ artifact, provider detection, strict no-fallback verification, artifact hashing, and a truthful CPU fallback. Actual Snapdragon NPU execution and performance remain pending compatible-device validation.”

## What is implemented now

- FP32 ONNX production model with full native-to-ONNX equivalence evidence.
- QDQ quantized candidate calibrated only on validation data.
- Runtime enumeration of available execution providers.
- QNN selection path for compatible environments.
- Strict verification designed to reject a purported QNN run if nodes silently fall back to CPU.
- Model/package hash gating and machine-readable runtime reporting.
- Visible CPU fallback and an explicit `snapdragon_npu_verified` state.

## What is not yet verified

- Execution on a physical Snapdragon X-series PC.
- QNN HTP/NPU provider selection on that device.
- ARM64 native packaging of the complete desktop application.
- Qualcomm AI Hub compile/profile job evidence.
- Device-measured latency, energy, battery, sustained thermals, or performance-per-watt.

## Why Snapdragon is a strong fit

SnapShield handles privacy-sensitive content that is useful even without connectivity: messages, screenshots, QR codes, and URLs. An integrated NPU can be a natural target for sustained local inference while leaving CPU resources available for the UI and deterministic security modules. Snapdragon PCs also align with the product’s local-first promise. Those are architectural motivations, not measured benefits in the current build.

## Why the CPU fallback matters

Security software must remain usable when a preferred accelerator is absent or unavailable. CPU fallback makes the product testable on ordinary machines and prevents provider availability from becoming a single point of failure. The UI exposes the fallback so portability does not become a misleading acceleration claim.

## Why not claim the NPU from the device name

A Snapdragon-branded machine does not prove that a particular graph executed on the NPU. Provider initialization can fail, unsupported operations can fall back, or the wrong artifact can load. SnapShield’s acceptance condition is evidence: QNN must be available and selected, the intended model hash must match, strict fallback checks must pass, and the report must identify the actual provider.

## Planned compatible-device validation protocol

1. Build and install the ARM64 application and pinned runtime dependencies.
2. Record device model, Windows build, firmware, driver, ONNX Runtime, and QNN versions.
3. Verify the packaged model hash against the approved artifact.
4. Run the provider capability check and capture the unedited report.
5. Execute the fixed text and multimodal corpus with strict CPU fallback disabled.
6. Confirm QNN/HTP provider selection and per-node assignment where supported.
7. Compare predictions with FP32 reference outputs and record disagreements.
8. Benchmark warm-up, median, P95, memory, sustained runs, and—only if instrumentation is available—power and thermals.
9. Archive commands, logs, reports, and screenshots with timestamps.
10. Promote the claim to “verified on Snapdragon NPU” only if every gate passes.

## If asked, “So is this really a Snapdragon project?”

Short answer: “Yes as a deployment architecture and implementation target; not yet as a verified NPU benchmark.”

Long answer: “The project contains more than a Snapdragon aspiration: it has a deployable ONNX graph, a quantized candidate, QNN-aware provider logic, strict fallback detection, and visible runtime truth. The missing step is physical-device evidence. We deliberately separate implemented readiness from completed hardware verification.”

## Claims table

| Claim | Status | Safe wording |
|---|---|---|
| Local ONNX inference | Verified | “The model executes locally through ONNX Runtime.” |
| CPU execution on development machine | Verified | “The audited build selected CPUExecutionProvider.” |
| QNN-compatible code path | Implemented | “A QNN provider path and strict verification gate are implemented.” |
| NPU-oriented quantized model | Prepared, not device-verified | “A QDQ candidate is prepared for compatible-device validation.” |
| Snapdragon NPU execution | Unverified | “Pending a real compatible-device QNN report.” |
| Snapdragon performance/power advantage | Unmeasured | Do not state a numeric or comparative benefit. |

## Phrases to avoid

- “Running on the Snapdragon NPU”
- “NPU accelerated”
- “Optimized by Qualcomm AI Hub”
- “Faster and more efficient on Snapdragon”
- “Production-ready ARM64 build”

Use those phrases only after the corresponding evidence exists.
