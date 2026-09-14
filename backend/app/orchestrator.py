import hashlib
import time
from typing import Any

from .database import create_incident
from .brand_analyzer import analyze_brand_mismatch
from .pii_analyzer import analyze_pii
from .risk_engine import explain, fuse, recommendations, severity_for
from .runtime import runtime_manager
from .text_analyzer import analyze_text
from .url_analyzer import analyze_url


def _hash(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def analyze_text_full(text: str, save: bool = True) -> dict[str, Any]:
    start = time.perf_counter()
    text_result = analyze_text(text)
    signals = list(text_result["signals"])
    url_results = []
    for url in text_result["urls"][:10]:
        try:
            finding = analyze_url(url)
            url_results.append(finding)
            signals.extend(finding["signals"])
        except ValueError:
            signals.append({"id": "URL_MALFORMED", "name": "Malformed URL", "severity": "moderate", "description": "A URL-like value could not be safely parsed.", "contribution": 7, "evidence": None})
    signals.extend(analyze_brand_mismatch(text_result["clean_text"], text_result["urls"]))
    pii, redacted = analyze_pii(text)
    if pii:
        signals.append({"id": "PII_PRESENT", "name": "Sensitive data present", "severity": "low", "description": "Potentially sensitive data was detected and redacted in the safe view.", "contribution": 3, "evidence": f"{len(pii)} finding(s)"})
    score = fuse(signals, text_result["probability"])
    result = {
        "id": None, "input_type": "text", "risk_score": score, "severity": severity_for(score),
        "threat_category": text_result["category"], "classification": "suspicious" if score >= 25 else "likely benign",
        "confidence": round(text_result["probability"], 4) if text_result["probability"] is not None else None,
        "signals": signals, "detected_urls": text_result["urls"], "pii_findings": pii, "redacted_text": redacted,
        "explanation": explain(score, text_result["category"], signals), "recommendations": recommendations(score, signals),
        "runtime": runtime_manager.metadata(), "processing_time_ms": round((time.perf_counter() - start) * 1000, 2),
        "privacy_status": "Processed locally; source content not persisted",
        "details": {"url_findings": url_results, "model": text_result["model"], "model_role": "Supporting signal; structured evidence controls score"},
    }
    if save: result["id"] = create_incident(result, _hash(text.encode("utf-8")))
    return result


def analyze_url_full(url: str, save: bool = True) -> dict[str, Any]:
    start = time.perf_counter()
    finding = analyze_url(url)
    score = fuse(finding["signals"])
    category = "Suspicious URL" if score >= 25 else "No specific URL threat detected"
    result = {
        "id": None, "input_type": "url", "risk_score": score, "severity": severity_for(score),
        "threat_category": category, "classification": "suspicious" if score >= 25 else "likely benign",
        "confidence": None, "signals": finding["signals"], "detected_urls": [finding["normalized_url"]],
        "pii_findings": [], "redacted_text": None, "explanation": explain(score, category, finding["signals"]),
        "recommendations": recommendations(score, finding["signals"]), "runtime": runtime_manager.metadata(),
        "processing_time_ms": round((time.perf_counter() - start) * 1000, 2), "privacy_status": "Analyzed locally; URL was not opened or contacted",
        "details": finding,
    }
    if save: result["id"] = create_incident(result, _hash(url.encode("utf-8")))
    return result
