from __future__ import annotations

import time
from functools import lru_cache
from typing import Any

import cv2
import numpy as np


@lru_cache(maxsize=1)
def get_ocr_engine():
    from rapidocr_onnxruntime import RapidOCR
    # Bound all three OCR ONNX sessions. Automatic 20-thread sessions caused
    # severe oversubscription on the development laptop during recognition.
    return RapidOCR(intra_op_num_threads=4, inter_op_num_threads=1, rec_batch_num=6)


def ocr_status() -> dict[str, Any]:
    try:
        get_ocr_engine()
        return {"available": True, "engine": "RapidOCR ONNX Runtime", "local": True}
    except Exception as exc:
        return {"available": False, "engine": "unavailable", "local": True, "error": type(exc).__name__}


def extract_text(content: bytes) -> dict[str, Any]:
    started = time.perf_counter()
    decoded = cv2.imdecode(np.frombuffer(content, dtype=np.uint8), cv2.IMREAD_COLOR)
    if decoded is None:
        raise ValueError("Image could not be decoded for OCR")
    result, engine_timing = get_ocr_engine()(decoded)
    lines = result or []
    text = "\n".join(str(item[1]) for item in lines).strip()
    confidences = [float(item[2]) for item in lines if len(item) >= 3]
    return {
        "engine": "RapidOCR ONNX Runtime", "available": True, "text": text,
        "characters": len(text), "line_count": len(lines),
        "confidence": round(sum(confidences) / len(confidences), 4) if confidences else None,
        "processing_time_ms": round((time.perf_counter() - started) * 1000, 2),
        "engine_timing_seconds": engine_timing,
    }
