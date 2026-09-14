# Snapdragon deployment and validation

## Current classification

### VERIFIED ON SNAPDRAGON

- Nothing yet. No Snapdragon device was available for this pass.

### IMPLEMENTED BUT HARDWARE VALIDATION PENDING

- ONNX Runtime provider discovery and explicit selected-provider reporting.
- FP32 ONNX classifier with QNN-friendly operators: `MatMul`, `Add`, `Sigmoid`.
- QDQ quantized candidate using `QuantizeLinear`/`DequantizeLinear`, QUInt8 activations, and QInt8 weights.
- CPU fallback if accelerated initialization is unavailable.
- Automated `scripts/snapdragon/validate_snapdragon.py` report with hardware, runtime, providers, model hash/operators, warm-up, 100 iterations, latency, memory delta, and output correctness.
- Conservative runtime gate: QDQ/QNN is selected only when the report is verified, the provider exists, and the reported filename/SHA-256 match the exact artifact; the QNN session disables CPU fallback.

### PLANNED / NOT IMPLEMENTED

- Native Windows ARM64 release artifact.
- QNN HTP/NPU execution with CPU fallback disabled.
- Qualcomm AI Hub compile/profile job and job reference; no account/credentials or hosted job were used.
- Named Snapdragon X Elite/Plus/X2 latency, sustained-load, memory, or power measurements.
- Code signing and a production installer/updater.

## Development-machine evidence

`benchmarks/results/snapdragon_validation.json` truthfully reports:

- Device: `LAPTOP-CDQCN56C`, Intel64 Family 6 Model 186, AMD64.
- OS: Windows 11 build 26200.
- ONNX Runtime: 1.30.0.
- Available providers: `AzureExecutionProvider`, `CPUExecutionProvider`.
- Selected provider: `CPUExecutionProvider`.
- QNN provider: unavailable; QNN SDK environment: absent.
- Result: `verified: false`.
- Reason: HTP verification requires native Windows ARM64, QNN EP, and a no-CPU-fallback run.

The 100-iteration CPU inference-only measurement is documented in [BENCHMARKS.md](BENCHMARKS.md). It is not a Snapdragon benchmark.

## Exact target validation procedure

1. Use an ARM64 Windows Snapdragon machine and record the exact SoC, OS build, firmware, and power mode.
2. Install a compatible ONNX Runtime QNN package or Windows ML QNN execution provider plus the required Qualcomm runtime.
3. Confirm `QNNExecutionProvider` is returned by `onnxruntime.get_available_providers()`.
4. Place the FP32 and QDQ artifacts plus vectorizer in `ml/artifacts`.
5. Run `python scripts/snapdragon/validate_snapdragon.py` first with the CPU reference.
6. Create the QNN session for HTP with CPU fallback disabled. A provider merely appearing in the list is not proof of graph assignment.
7. Confirm all nodes are assigned, compare target probabilities/classes against the CPU reference, and inspect runtime profiling.
8. Repeat cold and warm component benchmarks with identical inputs and iterations.
9. Set `verified: true` only after those checks pass; retain the generated report as evidence.

## Qualcomm AI Hub path

The simple numeric graph is suitable for a compile/profile attempt with the exact target device selected. Upload only SnapShield's own ONNX artifact and use an input specification equivalent to float32 `[1,10264]`. Preserve the job identifier, target device, runtime, compile options, profile output, and validation results. Do not reuse benchmarks from a different model. This workflow is pending credentials/hosted access.

## Why Snapdragon

Security inputs often contain sensitive account context, messages, screenshots, and credentials. Efficient on-device inference supports the product's privacy boundary and offline availability. Snapdragon is therefore a deployment target, not a retroactive performance claim.

Official references checked 2026-09-12:

- <https://www.qualcomm.com/developer/windows-on-snapdragon/windows-on-snapdragon-ai>
- <https://dev.aihub.qualcomm.com/docs/>
- <https://dev.aihub.qualcomm.com/docs/hub/compile_examples.html>
- <https://onnxruntime.ai/docs/execution-providers/QNN-ExecutionProvider.html>
- <https://learn.microsoft.com/windows/ai/new-windows-ml/get-started>
- <https://learn.microsoft.com/windows/ai/new-windows-ml/supported-execution-providers>
