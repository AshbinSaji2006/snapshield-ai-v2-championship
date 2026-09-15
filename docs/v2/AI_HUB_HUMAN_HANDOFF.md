# Qualcomm AI Hub Human Handoff

Status on 2026-09-15: **PENDING — local credentials are not configured.** No Qualcomm job has been submitted and no Snapdragon/NPU result is claimed.

## 1. Configure credentials securely

Request access at Qualcomm AI Hub, then run this locally from a trusted terminal:

```powershell
qai-hub configure --api_token YOUR_TOKEN
```

Do not paste the token into chat, source code, Git, screenshots, logs, or the command history used for a public demo. The SDK stores it in `%USERPROFILE%\.qai_hub\client.ini`; that file must never be committed.

Confirm authentication without displaying secrets:

```powershell
.\.venv\Scripts\qai-hub.exe list-devices
```

## 2. Execute the exact validation

```powershell
powershell -ExecutionPolicy Bypass -File .\scripts\snapdragon\run_aihub_validation.ps1
```

The script validates the SHA-256 recorded in `ml/v2/deep_guard/manifest.json`, selects the account-visible `Snapdragon X Elite CRD`, requests `precompiled_qnn_onnx` with NPU compute, downloads compile/profile logs, and refuses to mark VERIFIED unless structured compute-unit evidence contains only NPU/HTP values.

## 3. Expected outputs

- `reports/snapdragon/aihub/job_evidence.json`
- `reports/snapdragon/aihub/profile.json`
- compile and profile job logs
- `reports/snapdragon/aihub/snapshield_deep_guard_xelite.onnx`
- `benchmarks/results/snapdragon_validation.json`

The report records job IDs/URLs, device, SDK version, source and compiled hashes, execution-unit fields, and any failure.

## 4. Detect failure

- Exit 2: credentials are still missing; no job was submitted.
- Exit 1: a job failed or the profile did not prove NPU/HTP execution.
- Exit 0: exact-artifact compile/profile succeeded and structured execution-unit evidence passed the strict gate.

A successful job is not automatically proof of NPU execution. Inspect the saved profile and per-layer placement. CPU fallback must not be described as NPU.

## 5. Preserve evidence

Keep the raw profile, all downloaded logs, `job_evidence.json`, the compiled artifact, and job URLs. Do not hand-edit raw evidence. Generate SHA-256 checksums during the final release step.

## 6. Import into SnapShield

The runtime reads `benchmarks/results/snapdragon_validation.json`. A historical hosted profile does not make the current machine report QNN active: the application also requires an actual local `QNNExecutionProvider` session and the exact validated artifact before showing NPU active.

## 7. Rerun audits

After validation, rerun backend tests, frontend checks, the unified benchmarks, the claim-ledger check, and the final claim audit. Update public wording only from the exact device/runtime/result in the saved evidence.
