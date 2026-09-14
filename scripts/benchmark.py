"""Component-specific benchmarks; never conflates rules with ML latency."""
from __future__ import annotations

import json
import platform
import statistics
import sys
import time
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from backend.app.model_runtime import ONNXTextClassifier, get_classifier
from backend.app.ocr_engine import extract_text
from backend.app.orchestrator import analyze_text_full
from backend.app.pii_analyzer import analyze_pii
from backend.app.runtime import runtime_manager
from backend.app.url_analyzer import analyze_url

TEXT = "URGENT: Your SBI account is suspended. Verify your password at http://192.0.2.1:8080/sbi/login.exe"
URL = "http://192.0.2.1:8080/sbi/verify/login.exe"
IMAGE = ROOT / "data" / "samples" / "demo_screenshot.png"
MULTIMODAL = ROOT / "data" / "samples" / "demo_multimodal.png"
QR = ROOT / "data" / "samples" / "demo_qr.png"


def measure(name: str, function, iterations: int, warmups: int = 3) -> dict:
    for _ in range(warmups):
        function()
    values = []
    for _ in range(iterations):
        started = time.perf_counter(); function(); values.append((time.perf_counter() - started) * 1000)
    values.sort()
    return {"name": name, "iterations": iterations, "mean_ms": round(statistics.mean(values), 4), "median_ms": round(statistics.median(values), 4), "p95_ms": round(values[min(len(values)-1, int(len(values)*.95))], 4), "min_ms": round(values[0], 4), "max_ms": round(values[-1], 4)}


def main() -> None:
    classifier = get_classifier()
    features = classifier.vectorizer.transform([TEXT]).toarray().astype(np.float32)
    qr_image = cv2.imdecode(np.frombuffer(QR.read_bytes(), dtype=np.uint8), cv2.IMREAD_COLOR); detector = cv2.QRCodeDetector()
    results = [
        measure("Cold ONNX model + vectorizer load", lambda: ONNXTextClassifier(), 10, 0),
        measure("URL rule analysis", lambda: analyze_url(URL), 500),
        measure("Text preprocessing (TF-IDF)", lambda: classifier.vectorizer.transform([TEXT]), 300),
        measure("Text ONNX inference only", lambda: classifier.session.run(["probability"], {"features": features}), 500) if hasattr(classifier, "session") else measure("Text sklearn inference only", lambda: classifier.classifier.predict_proba(classifier.vectorizer.transform([TEXT])), 500),
        measure("PII detection and redaction", lambda: analyze_pii(TEXT + " priya@example.com 4111 1111 1111 1111"), 500),
        measure("QR decode", lambda: detector.detectAndDecode(qr_image), 100),
        measure("Full text pipeline", lambda: analyze_text_full(TEXT, False), 200),
    ]
    if IMAGE.exists():
        payload = IMAGE.read_bytes()
        results.append(measure("OCR screenshot", lambda: extract_text(payload), 10, 1))
        results.append(measure("Full screenshot OCR + security pipeline", lambda: analyze_text_full(extract_text(payload)["text"], False), 10, 1))
    if MULTIMODAL.exists():
        multimodal_payload = MULTIMODAL.read_bytes()
        multimodal_image = cv2.imdecode(np.frombuffer(multimodal_payload, dtype=np.uint8), cv2.IMREAD_COLOR)
        def full_multimodal():
            ocr_text = extract_text(multimodal_payload)["text"]
            qr_text = cv2.QRCodeDetector().detectAndDecode(multimodal_image)[0]
            return analyze_text_full("\n".join(value for value in (ocr_text, qr_text) if value), False)
        results.append(measure("Full multimodal OCR + QR + security pipeline", full_multimodal, 10, 1))
    report = {"timestamp": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "machine": platform.platform(), "architecture": platform.machine(), "python": platform.python_version(), "provider": runtime_manager.selected_provider, "model": getattr(classifier, "model_path", Path("sklearn")).name, "warm_benchmark": True, "snapdragon_npu_verified": runtime_manager.metadata()["snapdragon_npu_verified"], "results": results}
    output = ROOT / "benchmarks" / "results" / "component_benchmark.json"; output.parent.mkdir(parents=True, exist_ok=True); output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
