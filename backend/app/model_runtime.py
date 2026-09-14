from __future__ import annotations

import json
import hashlib
import logging
import time
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import joblib
import numpy as np

from .runtime import runtime_manager

logger = logging.getLogger("snapshield.model")
ROOT = Path(__file__).resolve().parents[2]
ARTIFACTS = ROOT / "ml" / "artifacts"


def _validated_qnn_candidate(available: list[str], path: Path) -> bool:
    validation = runtime_manager.snapdragon_validation()
    if not (validation.get("verified") is True and validation.get("execution_provider") == "QNNExecutionProvider"):
        return False
    if "QNNExecutionProvider" not in available or validation.get("model") != path.name or not path.is_file():
        return False
    return validation.get("model_sha256") == hashlib.sha256(path.read_bytes()).hexdigest()


@dataclass(frozen=True)
class Prediction:
    probability: float
    provider: str
    preprocessing_ms: float
    inference_ms: float
    model_version: str


class ONNXTextClassifier:
    def __init__(self) -> None:
        import onnxruntime as ort

        self.vectorizer = joblib.load(ARTIFACTS / "text_vectorizer.joblib")
        metadata_path = ARTIFACTS / "model_metadata.json"
        self.metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        available = ort.get_available_providers()
        qdq_path = ARTIFACTS / "text_classifier.qdq.onnx"
        model_path = ARTIFACTS / "text_classifier.onnx"
        providers = [provider for provider in ("DmlExecutionProvider", "CUDAExecutionProvider", "CPUExecutionProvider") if provider in available]
        if not providers:
            raise RuntimeError("No supported ONNX Runtime provider is available")
        if _validated_qnn_candidate(available, qdq_path):
            options = ort.SessionOptions()
            options.add_session_config_entry("session.disable_cpu_ep_fallback", "1")
            try:
                self.session = ort.InferenceSession(str(qdq_path), sess_options=options, providers=[("QNNExecutionProvider", {"backend_type": "htp"})])
                model_path = qdq_path
            except Exception as exc:
                logger.warning("Verified QNN session failed; using FP32 ONNX fallback: %s", type(exc).__name__)
                self.session = ort.InferenceSession(str(model_path), providers=providers)
        else:
            self.session = ort.InferenceSession(str(model_path), providers=providers)
        self.provider = self.session.get_providers()[0]
        self.model_path = model_path
        runtime_manager.record_model_provider(self.provider)
        logger.info("Loaded local text model version=%s provider=%s", self.metadata["version"], self.provider)

    def predict(self, text: str) -> Prediction:
        started = time.perf_counter()
        features = self.vectorizer.transform([text]).toarray().astype(np.float32)
        pre_ms = (time.perf_counter() - started) * 1000
        infer_started = time.perf_counter()
        probability = float(self.session.run(["probability"], {"features": features})[0][0, 0])
        inference_ms = (time.perf_counter() - infer_started) * 1000
        return Prediction(probability, self.provider, pre_ms, inference_ms, self.metadata["version"])


class SklearnTextClassifier:
    """Artifact fallback used only when ONNX Runtime cannot initialize."""
    def __init__(self) -> None:
        self.vectorizer = joblib.load(ARTIFACTS / "text_vectorizer.joblib")
        self.classifier = joblib.load(ARTIFACTS / "text_classifier.joblib")
        self.metadata = json.loads((ARTIFACTS / "model_metadata.json").read_text(encoding="utf-8"))
        self.provider = "scikit-learn CPU fallback"
        runtime_manager.record_model_provider(self.provider)

    def predict(self, text: str) -> Prediction:
        started = time.perf_counter(); features = self.vectorizer.transform([text]); pre_ms = (time.perf_counter() - started) * 1000
        infer_started = time.perf_counter(); probability = float(self.classifier.predict_proba(features)[0, 1]); inference_ms = (time.perf_counter() - infer_started) * 1000
        return Prediction(probability, self.provider, pre_ms, inference_ms, self.metadata["version"])


@lru_cache(maxsize=1)
def get_classifier() -> ONNXTextClassifier | SklearnTextClassifier:
    try:
        return ONNXTextClassifier()
    except Exception as exc:
        logger.warning("ONNX model initialization failed; using local sklearn fallback: %s", type(exc).__name__)
        return SklearnTextClassifier()


def model_status() -> dict:
    classifier = get_classifier()
    return {"name": classifier.metadata["model_name"], "version": classifier.metadata["version"], "provider": classifier.provider, "onnx": isinstance(classifier, ONNXTextClassifier), "model_file": classifier.model_path.name if isinstance(classifier, ONNXTextClassifier) else "text_classifier.joblib"}
