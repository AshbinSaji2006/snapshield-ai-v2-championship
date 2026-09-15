# Snapdragon Validation Report

Report date: 2026-09-15

## VERIFIED

- The selected Deep Guard is exported to FP32 ONNX opset 17 and executes locally with `CPUExecutionProvider`.
- FP32 ONNX class agreement is 100% across 766 validation messages.
- A static INT8 QDQ candidate preserves 100% FP32 class agreement on both the 766-message UCI test and 521-message cross-domain set.
- The deployment architecture has explicit artifact hashes and rejects stale or mismatched artifacts.

## IMPLEMENTED BUT NOT VERIFIED

- Qualcomm AI Hub compile/profile automation for the exact QDQ artifact.
- Requested target: `Snapdragon X Elite CRD`.
- Requested target runtime/compute: `precompiled_qnn_onnx`, NPU.
- Strict evidence gate that saves raw logs/profile and requires explicit structured NPU/HTP placement.
- Local runtime guard that does not infer current NPU use from provider availability or historical evidence.

## PENDING

- `AI_HUB_AUTH`: local `%USERPROFILE%/.qai_hub/client.ini` is absent.
- Qualcomm-hosted compile job ID and compiled artifact.
- Qualcomm-hosted profile job, latency, memory and per-layer execution-unit evidence.
- Local Windows-on-Snapdragon QNN session validation.

## NOT IMPLEMENTED

- No measured Snapdragon power, energy, battery or thermal result.
- No native ARM64 Windows executable built on this AMD64 development machine.

Allowed wording today: **Designed for Snapdragon-powered PCs. Snapdragon-ready ONNX/QNN validation workflow; hardware validation pending.**

Forbidden wording today: **NPU verified**, **running on Snapdragon NPU**, **NPU accelerated**, or any Snapdragon latency/power number.
