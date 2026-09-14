import re
from .model_runtime import get_classifier
URL_RE = re.compile(r"(?i)\b(?:https?\s*://|hxxps?\s*:\s*//|www\.)[^\s<>\"']+")

RULES = [
    ("TXT_URGENCY", "Urgency pressure", "moderate", r"\b(urgent|immediately|act now|within \d+ hours?|final warning|expires? today)\b", 10, "Creates time pressure."),
    ("TXT_ACCOUNT_THREAT", "Account threat", "high", r"\b(account|profile).{0,30}(suspend|lock|disable|close|restrict)", 16, "Threatens loss of account access."),
    ("TXT_CREDENTIAL", "Credential request", "high", r"\b(verify|confirm|enter|send|share|provide).{0,35}(password|p\s*a\s*s\s*s\s*w\s*o\s*r\s*d|credential|login|username|pin)\b", 22, "Requests authentication information."),
    ("TXT_OTP", "One-time code request", "critical", r"\b(otp|one[ -]?time (?:password|code)|verification code)\b", 24, "Mentions a one-time authentication code."),
    ("TXT_PAYMENT", "Payment request", "high", r"\b(pay|payment|wire|transfer|invoice|gift cards?|crypto|bitcoin|wallet)\b", 14, "Contains payment or irreversible-transfer language."),
    ("TXT_PRIZE", "Prize or financial lure", "high", r"\b(winner|won|lottery|prize|inheritance|guaranteed return|double your)\b", 18, "Uses an unexpected reward or investment lure."),
    ("TXT_DELIVERY", "Delivery lure", "moderate", r"\b(package|parcel|delivery|shipping).{0,35}(fee|failed|held|address|reschedule)\b", 12, "Uses a delivery problem as a call to action."),
    ("TXT_AUTHORITY", "Authority impersonation", "moderate", r"\b(ceo|director|police|tax department|irs|government|bank security|support team)\b", 10, "Invokes authority or support staff."),
    ("TXT_REMOTE", "Remote support request", "high", r"\b(anydesk|teamviewer|remote access|screen share|support tool)\b", 20, "Requests remote access or support software."),
    ("TXT_SECRET", "Secrecy pressure", "moderate", r"\b(do not tell|keep this confidential|don't contact|secret)\b", 10, "Attempts to isolate the recipient."),
]


def analyze_text(text: str) -> dict:
    had_zero_width = any(character in text for character in "\u200b\u200c\u200d\ufeff")
    clean = text.replace("\u200b", "").replace("\u200c", "").replace("\u200d", "")
    signals = []
    if had_zero_width:
        signals.append({"id": "TXT_ZERO_WIDTH", "name": "Zero-width obfuscation", "severity": "moderate", "description": "Invisible Unicode characters were removed before analysis; these can be used to evade filters.", "contribution": 9, "evidence": "Invisible characters normalized"})
    mixed_script = next((token for token in re.findall(r"\w+", clean) if re.search(r"[A-Za-z]", token) and re.search(r"[\u0400-\u04ff\u0370-\u03ff]", token)), None)
    if mixed_script:
        signals.append({"id": "TXT_MIXED_SCRIPT", "name": "Mixed-script look-alike text", "severity": "moderate", "description": "A word mixes Latin with Cyrillic or Greek characters, which can create visual impersonation.", "contribution": 11, "evidence": mixed_script[:90]})
    security_advice = bool(re.search(r"\b(?:never|do not|don't)\s+(?:ask.{0,35}to\s+)?share\b", clean, re.I))
    if security_advice:
        signals.append({"id": "TXT_SAFETY_ADVICE", "name": "Protective security advice", "severity": "info", "description": "The message warns against sharing authentication data rather than requesting it.", "contribution": 0, "evidence": "Negated request context detected"})
    category_points: dict[str, int] = {}
    for code, name, severity, pattern, points, description in RULES:
        if security_advice and code in {"TXT_CREDENTIAL", "TXT_OTP"}:
            continue
        match = re.search(pattern, clean, re.I | re.S)
        if match:
            evidence = match.group(0)[:90]
            signals.append({"id": code, "name": name, "severity": severity, "description": description, "contribution": points, "evidence": evidence, "span": {"start": match.start(), "end": match.end()}})
            category_points[name] = points
    urls = list(dict.fromkeys(m.group(0).rstrip(".,;:!?)") for m in URL_RE.finditer(clean)))
    prediction = get_classifier().predict(clean)
    probability = prediction.probability
    if probability is not None and probability >= 0.65:
        contribution = round(8 + probability * 17, 1)
        signals.append({"id": "TXT_ML_PHISHING", "name": "Local ML phishing pattern", "severity": "high" if probability >= .8 else "moderate", "description": "The local TF-IDF logistic classifier found language patterns similar to its phishing examples.", "contribution": contribution, "evidence": f"model probability {probability:.2f}"})
    elif probability is not None and probability <= 0.25:
        signals.append({"id": "TXT_ML_BENIGN", "name": "Local ML benign pattern", "severity": "info", "description": "Language resembles benign examples in the bundled model data.", "contribution": 0, "evidence": f"model probability {probability:.2f}"})
    top = max(category_points, key=category_points.get) if category_points else "Suspicious communication" if signals else "No specific threat detected"
    return {"clean_text": clean, "urls": urls, "signals": signals, "probability": probability, "category": top, "model": {"provider": prediction.provider, "version": prediction.model_version, "preprocessing_ms": round(prediction.preprocessing_ms, 3), "inference_ms": round(prediction.inference_ms, 3)}}
