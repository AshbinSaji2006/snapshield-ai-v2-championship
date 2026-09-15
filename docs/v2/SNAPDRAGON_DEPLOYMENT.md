# Snapdragon Deployment

Deep Guard ships as fixed-shape `[1,128]` FP32 ONNX opset 17 with `input_ids` and `attention_mask` int32 inputs. A representative 256-record validation calibration partition produced a static INT8 QDQ MatMul/Gemm candidate. The QDQ artifact is 16,395,032 bytes versus 17,515,277 bytes FP32 and preserved 100% class agreement on both final evaluation sets; its largest observed UCI probability delta was 0.03219.

The current machine runs both guards with `CPUExecutionProvider`. `scripts/snapdragon/run_aihub_validation.py` verifies the QDQ hash, requests the account-visible `Snapdragon X Elite CRD`, compiles to `precompiled_qnn_onnx` for NPU compute, profiles the compiled model, downloads raw logs/profile/artifact, and only marks validation true when structured per-layer compute-unit fields explicitly show NPU/HTP without CPU/GPU.

Local runtime activation is stricter still: historical hosted validation cannot make the current process claim NPU. SnapShield requires a matching compiled artifact, matching validation hash, an available `QNNExecutionProvider`, a strict session with CPU fallback disabled, and successful session initialization. Any failure returns to FP32 CPU and reports that provider.

Current status: **IMPLEMENTED BUT UNVERIFIED; AI Hub authentication pending.** See `AI_HUB_HUMAN_HANDOFF.md` and `reports/snapdragon/SNAPDRAGON_VALIDATION_REPORT.md`.
