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
from .normalization import normalize_security, normalization_signals
from .india_security import india_signals
from .adaptive import route
from .deep_guard import get_deep_guard, calibrated_fast
from .evidence_graph import build_graph


def _hash(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def analyze_text_full(text: str, save: bool = True, context: dict | None = None) -> dict[str, Any]:
    start = time.perf_counter()
    normalized = normalize_security(text)
    text_result = analyze_text(normalized.normalized_security_text)
    signals = list(text_result["signals"])
    signals.extend(normalization_signals(normalized))
    signals.extend(india_signals(normalized.normalized_security_text))
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
    context = context or {}
    fast_probability = calibrated_fast(text_result["probability"])
    routing = route(fast_probability, signals, script=normalized.script, qr=bool(context.get("qr")), ocr_confidence=context.get("ocr_confidence"))
    deep = get_deep_guard()
    deep_result = deep.predict(normalized.normalized_security_text) if routing["requested_deep"] else None
    routing["deep_executed"] = deep_result is not None
    routing["path"] = "deep" if deep_result else "fast_fallback" if routing["requested_deep"] else "fast"
    if routing["requested_deep"] and deep_result is None:
        routing["reasons"].append(deep.reason if not deep.ready else "Deep Guard inference failed; Fast Guard result retained")
    if deep_result and deep_result["truncated"]:
        routing["reasons"].append("Deep Guard read the first 128 tokens; full-text security rules still ran")
    if deep_result:
        signals = [s for s in signals if not s["id"].startswith("TXT_ML_")]
        if deep_result["probability"] >= .65:
            signals.append({"id":"DEEP_ML_RISK","name":"Deep Guard message-risk signal","severity":"high","description":"The selected local neural classifier detected spam-like message patterns; it is one supporting signal, not proof of phishing.","contribution":round(8+deep_result["probability"]*17,1),"evidence":f'Calibrated message-class probability {deep_result["probability"]:.3f}',"provenance":"Deep Guard ONNX"})
        else:
            signals.append({"id":"DEEP_ML_CLEAR","name":"Deep Guard low message-risk signal","severity":"info","description":"The selected local neural classifier did not identify a strong spam-like message pattern; deterministic evidence is still evaluated independently.","contribution":0,"evidence":f'Calibrated message-class probability {deep_result["probability"]:.3f}',"provenance":"Deep Guard ONNX"})
    # One contribution per rule; repeated URLs/brands do not multiply the same finding.
    unique = {}
    for signal in signals:
        key = signal["id"]
        if key not in unique or signal["contribution"] > unique[key]["contribution"]: unique[key] = signal
    signals = list(unique.values())
    decision_probability = deep_result["probability"] if deep_result else fast_probability
    score = fuse(signals, decision_probability)
    result = {
        "id": None, "input_type": context.get("input_type","text"), "risk_score": score, "severity": severity_for(score),
        "threat_category": text_result["category"], "classification": "suspicious" if score >= 25 else "likely benign",
        "confidence": round(decision_probability, 4) if decision_probability is not None else None,
        "signals": signals, "detected_urls": text_result["urls"], "pii_findings": pii, "redacted_text": redacted,
        "explanation": explain(score, text_result["category"], signals), "recommendations": recommendations(score, signals),
        "runtime": runtime_manager.metadata(), "processing_time_ms": round((time.perf_counter() - start) * 1000, 2),
        "privacy_status": "Processed locally; source content not persisted",
        "details": {"url_findings": url_results, "model": text_result["model"], "model_role": "Supporting signal; structured evidence controls score", "analysis_version":"2.0.0", "routing":routing,
                    "fast_guard":{"raw_probability":text_result["probability"],"calibrated_probability":fast_probability},"deep_guard":deep_result or deep.status(),
                    "normalization":{"original_text_redacted":redacted,"normalized_security_text_redacted":analyze_pii(normalized.normalized_security_text)[1],"transformations":list(normalized.transformations),"script":normalized.script,"span_coordinate_space":"normalized security text"},
                    "risk_score_type":"Ordinal evidence index; not a calibrated probability"},
    }
    result["details"]["evidence_graph"] = build_graph(result, context.get("sources") or [{"kind":"TextEvidence","label":"Submitted text","text":text}])
    result["processing_time_ms"] = round((time.perf_counter()-start)*1000,2)
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
    result["details"]["routing"] = {"path":"fast", "deep_executed":False,"reasons":["URL-only structural analysis; no neural text escalation required"]}
    result["details"]["evidence_graph"] = build_graph(result,[{"kind":"TextEvidence","label":"Submitted URL","text":url}])
    if save: result["id"] = create_incident(result, _hash(url.encode("utf-8")))
    return result
