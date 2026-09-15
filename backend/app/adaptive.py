"""Policy routing uses calibrated uncertainty and independent contextual evidence."""
import math
import json
from functools import lru_cache
from pathlib import Path

ROOT=Path(__file__).resolve().parents[2]

@lru_cache(maxsize=1)
def policy():
    try:
        value=json.loads((ROOT/"ml/v2/router_policy.json").read_text(encoding="utf-8"))
        return value if value.get("policy_version")=="adaptive-v2.2" else {}
    except (OSError,ValueError):
        return {}

def route(probability, signals, *, script="Latin", qr=False, ocr_confidence=None, truncated=False):
    ids={s["id"] for s in signals}
    p=.5 if probability is None else min(max(probability,1e-8),1-1e-8)
    entropy=-(p*math.log2(p)+(1-p)*math.log2(1-p))
    reasons=[]
    if probability is None: reasons.append("Fast Guard unavailable; deeper evidence requested")
    threshold=float(policy().get("entropy_threshold",.045))
    if probability is not None and entropy>=threshold: reasons.append("Fast Guard is outside the calibrated extreme-confidence bounds")
    credential=bool(ids & {"TXT_CREDENTIAL","TXT_OTP","INDIA_CREDENTIAL"})
    contextual=any(i.startswith(("URL_","BRAND_")) for i in ids)
    if credential and contextual: reasons.append("Credential solicitation co-occurs with URL or brand evidence")
    if any(i.startswith("NORM_") or i in {"TXT_ZERO_WIDTH","TXT_MIXED_SCRIPT"} for i in ids): reasons.append("Text contains security-relevant obfuscation")
    if qr and contextual: reasons.append("QR payload requires security correlation")
    if ocr_confidence is not None and ocr_confidence<.80: reasons.append("OCR confidence is low; visual evidence needs caution")
    if p<.25 and sum(float(s["contribution"]) for s in signals)>=40: reasons.append("Fast Guard and deterministic evidence disagree")
    unsupported="Devanagari" in script or "unsupported" in script
    if unsupported: reasons.append("English model coverage is limited for this script; deterministic checks retained")
    if truncated: reasons.append("Input exceeds Deep Guard token window; full-text rules remain active")
    requested=bool(reasons) and not unsupported
    decision_class="ESCALATE_UNCERTAIN" if requested else "FAST_ONLY_SAFE" if p<=.005 else "FAST_ONLY_HIGH_CONFIDENCE"
    if requested and any("co-occurs" in reason for reason in reasons): decision_class="ESCALATE_HIGH_RISK_CONTEXT"
    if requested and qr: decision_class="ESCALATE_MULTIMODAL"
    return {"policy_version":"adaptive-v2.2", "requested_deep":requested,"path":"deep_requested" if requested else "fast",
            "decision_class":decision_class,"entropy_threshold":threshold,
            "reasons":reasons or ["Low Fast Guard uncertainty and no high-risk contextual trigger"],
            "entropy_bits":round(entropy,5),"supported_neural_language":not unsupported,
            "risk_probability_warning":"Message-class probability is distinct from the evidence-based risk score"}
