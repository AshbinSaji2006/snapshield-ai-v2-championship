"""Compile/profile the exact Deep Guard QDQ artifact on a hosted Snapdragon PC.

Requires a separately configured ~/.qai_hub/client.ini. Never accepts or prints a token.
"""
from __future__ import annotations

import hashlib
import json
from pathlib import Path
import platform
import sys

import qai_hub as hub

ROOT = Path(__file__).resolve().parents[2]
MODEL_DIR = ROOT / "ml/v2/deep_guard"
OUT = ROOT / "reports/snapdragon/aihub"
VALIDATION = ROOT / "benchmarks/results/snapdragon_validation.json"
DEVICE_NAME = "Snapdragon X Elite CRD"


def sha(path: Path) -> str:
    with path.open("rb") as stream:
        return hashlib.file_digest(stream, "sha256").hexdigest()


def collect_units(value, units: list[str]) -> None:
    if isinstance(value, dict):
        for key, child in value.items():
            if key.lower() in {"compute_unit", "execution_unit", "computeunit", "unit"} and isinstance(child, str):
                units.append(child)
            collect_units(child, units)
    elif isinstance(value, list):
        for child in value: collect_units(child, units)


def main() -> int:
    config = Path.home() / ".qai_hub/client.ini"
    if not config.is_file():
        print("AI_HUB_AUTH=PENDING: configure the client locally; no job was submitted.")
        return 2
    manifest_path = MODEL_DIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    candidate_name = manifest.get("qnn_candidate")
    if not candidate_name:
        raise RuntimeError("No quantized artifact passed the local QNN-candidate gate")
    candidate = MODEL_DIR / candidate_name
    if sha(candidate) != manifest["file_hashes"].get(candidate_name):
        raise RuntimeError("QNN candidate hash does not match the deployment manifest")

    client = hub.Client()
    devices = client.get_devices(name=DEVICE_NAME)
    if not devices:
        raise RuntimeError(f"Hosted device not available to this account: {DEVICE_NAME}")
    device = devices[0]
    OUT.mkdir(parents=True, exist_ok=True); VALIDATION.parent.mkdir(parents=True, exist_ok=True)
    evidence = {"verified": False, "source_model": candidate.name, "model_sha256": sha(candidate),
                "device_requested": DEVICE_NAME, "qai_hub_version": hub.__version__,
                "developer_host": {"os": platform.platform(), "architecture": platform.machine()}}
    try:
        compile_job = client.submit_compile_job(candidate, device=device, name="SnapShield Deep Guard QDQ — X Elite",
                                                input_specs={"input_ids": ((1, 128), "int32"), "attention_mask": ((1, 128), "int32")},
                                                options="--target_runtime precompiled_qnn_onnx --compute_unit npu")
        evidence.update({"compile_job_id": compile_job.job_id, "compile_job_url": compile_job.url})
        status = compile_job.wait()
        compile_job.download_job_logs(str(OUT / "compile_logs"))
        if not status.success:
            raise RuntimeError(f"Compile job failed: {status.message}")
        compiled = OUT / "snapshield_deep_guard_xelite.onnx"
        compile_job.download_target_model(str(compiled))
        evidence["compiled_artifact_sha256"] = sha(compiled)
        profile_job = client.submit_profile_job(compile_job.get_target_model(), device=device,
                                                name="SnapShield Deep Guard QDQ — NPU profile", options="--compute_unit npu")
        evidence.update({"profile_job_id": profile_job.job_id, "profile_job_url": profile_job.url})
        profile_status = profile_job.wait()
        profile_job.download_job_logs(str(OUT / "profile_logs"))
        if not profile_status.success:
            raise RuntimeError(f"Profile job failed: {profile_status.message}")
        profile = profile_job.download_profile(str(OUT / "profile.json"))
        if isinstance(profile, str):
            profile = json.loads(Path(profile).read_text(encoding="utf-8"))
        units: list[str] = []; collect_units(profile, units)
        normalized_units = sorted(set(unit.upper() for unit in units))
        explicit_npu = bool(normalized_units) and all(("NPU" in unit or "HTP" in unit) and "CPU" not in unit and "GPU" not in unit for unit in normalized_units)
        evidence.update({"execution_provider": "QNNExecutionProvider" if explicit_npu else "UNVERIFIED",
                         "execution_units_found": normalized_units, "profile_evidence_saved": True,
                         "verified": bool(explicit_npu),
                         "verification_note": "All structured per-layer compute-unit fields report NPU/HTP" if explicit_npu else "Job succeeded, but structured profile did not prove exclusive NPU/HTP execution"})
    except Exception as exc:
        evidence.update({"verified": False, "failure_type": type(exc).__name__, "failure": str(exc)})
    (OUT / "job_evidence.json").write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    VALIDATION.write_text(json.dumps(evidence, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in evidence.items() if "token" not in k.lower()}, indent=2))
    return 0 if evidence["verified"] else 1


if __name__ == "__main__":
    sys.exit(main())
