import importlib.util
import os
import platform
import sys
import time
import json
from pathlib import Path
from typing import Any


class RuntimeManager:
    """Reports only providers that can be verified in the current process."""

    def __init__(self) -> None:
        self.started_at = time.time()
        self.onnx_providers: list[str] = []
        self.model_provider: str | None = None
        self._detect()

    def _detect(self) -> None:
        if importlib.util.find_spec("onnxruntime"):
            try:
                import onnxruntime as ort
                self.onnx_providers = ort.get_available_providers()
            except Exception:
                self.onnx_providers = []

    @property
    def selected_provider(self) -> str:
        return self.model_provider or ("CPUExecutionProvider" if "CPUExecutionProvider" in self.onnx_providers else "Native Python CPU")

    def record_model_provider(self, provider: str) -> None:
        self.model_provider = provider

    def snapdragon_validation(self) -> dict[str, Any]:
        path = Path(__file__).resolve().parents[2] / "benchmarks" / "results" / "snapdragon_validation.json"
        if not path.exists():
            return {"verified": False}
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except (OSError, json.JSONDecodeError):
            return {"verified": False}

    def metadata(self) -> dict[str, Any]:
        validation = self.snapdragon_validation()
        # A historical validation JSON cannot turn current CPU fallback into NPU execution.
        snapdragon_verified = bool(validation.get("verified")) and validation.get("execution_provider") == "QNNExecutionProvider" and self.selected_provider == "QNNExecutionProvider"
        return {
            "os": platform.platform(),
            "architecture": platform.machine(),
            "python": sys.version.split()[0],
            "onnx_available": bool(self.onnx_providers),
            "available_onnx_providers": self.onnx_providers,
            "selected_provider": self.selected_provider,
            "model_readiness": "ready (local hybrid classifier)",
            "snapdragon_npu_verified": snapdragon_verified,
            "snapdragon_status": "VERIFIED" if snapdragon_verified else "READY FOR SNAPDRAGON VALIDATION",
            "cloud_ai_enabled": False,
            "hardware_acceleration": "verified QNN NPU" if snapdragon_verified else "not detected" if self.selected_provider in {"CPUExecutionProvider", "Native Python CPU", "scikit-learn CPU fallback"} else self.selected_provider,
            "snapdragon_validation": validation,
            "process_id": os.getpid(),
        }


runtime_manager = RuntimeManager()
