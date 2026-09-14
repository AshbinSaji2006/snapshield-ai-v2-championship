"""Truthful QNN/Snapdragon validation with CPU fallback disabled for verification."""
from __future__ import annotations

import hashlib
import json
import os
import platform
import statistics
import sys
import time
from pathlib import Path

import joblib
import numpy as np
import onnx
import onnxruntime as ort
import psutil

ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "ml" / "artifacts"
OUTPUT = ROOT / "benchmarks" / "results" / "snapdragon_validation.json"
ITERATIONS = 100


def percentile(values: list[float], fraction: float) -> float:
    return sorted(values)[min(len(values) - 1, int(len(values) * fraction))]


def main() -> None:
    architecture = platform.machine()
    available = ort.get_available_providers()
    qnn_available = "QNNExecutionProvider" in available
    native_arm64 = architecture.upper() in {"ARM64", "AARCH64"}
    qnn_sdk = os.environ.get("QNN_SDK_ROOT") or os.environ.get("QAIRT_SDK_ROOT")
    vectorizer = joblib.load(ARTIFACTS / "text_vectorizer.joblib")
    sample = "URGENT: Your SBI account is suspended. Verify your password immediately."
    features = vectorizer.transform([sample]).toarray().astype(np.float32)
    reference = ort.InferenceSession(str(ARTIFACTS / "text_classifier.onnx"), providers=["CPUExecutionProvider"])
    expected = float(reference.run(["probability"], {"features": features})[0][0, 0])
    target = ARTIFACTS / ("text_classifier.qdq.onnx" if qnn_available and native_arm64 else "text_classifier.onnx")
    verified = False; error = None; selected = "CPUExecutionProvider"
    try:
        if qnn_available and native_arm64:
            options = ort.SessionOptions(); options.add_session_config_entry("session.disable_cpu_ep_fallback", "1")
            session = ort.InferenceSession(str(target), sess_options=options, providers=[("QNNExecutionProvider", {"backend_type": "htp"})])
            selected = "QNNExecutionProvider"
        else:
            session = reference
        for _ in range(10): session.run(["probability"], {"features": features})
        memory_before = psutil.Process().memory_info().rss; timings = []
        for _ in range(ITERATIONS):
            started = time.perf_counter(); actual = float(session.run(["probability"], {"features": features})[0][0, 0]); timings.append((time.perf_counter() - started) * 1000)
        memory_after = psutil.Process().memory_info().rss
        agreement = abs(expected - actual) <= 0.15 and (expected >= .5) == (actual >= .5)
        verified = bool(qnn_available and native_arm64 and selected == "QNNExecutionProvider" and agreement)
    except Exception as exc:
        timings = []; actual = None; memory_before = memory_after = psutil.Process().memory_info().rss
        agreement = False; error = f"{type(exc).__name__}: {exc}"
    model = onnx.load(target)
    report = {
        "verified": verified, "timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "device": platform.node() or "unknown",
        "chipset": os.environ.get("PROCESSOR_IDENTIFIER") or platform.processor() or "unknown", "architecture": architecture,
        "os": platform.platform(), "runtime": f"ONNX Runtime {ort.__version__}", "available_providers": available,
        "execution_provider": selected, "qnn_provider_available": qnn_available, "qnn_sdk_environment": qnn_sdk,
        "model": target.name, "model_sha256": hashlib.sha256(target.read_bytes()).hexdigest(),
        "onnx_operators": sorted({node.op_type for node in model.graph.node}), "iterations": len(timings),
        "mean_latency_ms": round(statistics.mean(timings), 4) if timings else None, "median_latency_ms": round(statistics.median(timings), 4) if timings else None,
        "p95_latency_ms": round(percentile(timings, .95), 4) if timings else None, "min_latency_ms": round(min(timings), 4) if timings else None,
        "max_latency_ms": round(max(timings), 4) if timings else None, "memory_delta_bytes": memory_after - memory_before,
        "reference_probability": expected, "target_probability": actual, "output_correctness": agreement,
        "reason_not_verified": None if verified else error or "QNN HTP verification requires native Windows ARM64, QNNExecutionProvider, and a no-CPU-fallback inference run.",
    }
    OUTPUT.parent.mkdir(parents=True, exist_ok=True); OUTPUT.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if qnn_available and native_arm64 and not verified: raise SystemExit(2)


if __name__ == "__main__": main()
