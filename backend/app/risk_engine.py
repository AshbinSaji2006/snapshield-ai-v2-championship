from typing import Any


def severity_for(score: int) -> str:
    if score >= 75: return "critical"
    if score >= 50: return "high"
    if score >= 25: return "moderate"
    return "low"


def fuse(signals: list[dict[str, Any]], ml_probability: float | None = None) -> int:
    families = {"model": [], "url": [], "brand": [], "normalization": [], "regional": [], "privacy": [], "social": []}
    ids = set()
    for signal in signals:
        contribution = float(signal["contribution"])
        if contribution <= 0: continue
        code = signal.get("id", "UNSCOPED"); ids.add(code)
        family = "model" if code.startswith(("TXT_ML_", "DEEP_ML_")) else "url" if code.startswith("URL_") else "brand" if code.startswith("BRAND_") else "normalization" if code.startswith("NORM_") or code in {"TXT_ZERO_WIDTH", "TXT_MIXED_SCRIPT"} else "regional" if code.startswith("INDIA_") else "privacy" if code == "PII_PRESENT" else "social"
        families[family].append(contribution)
    caps = {"model":25,"url":45,"brand":30,"normalization":15,"regional":30,"privacy":3,"social":45}
    raw = sum(min(caps[name], sum(values)) for name,values in families.items())
    # Explicit corroboration rules elevate combinations; no single heuristic proves harm.
    credential = bool(ids & {"TXT_CREDENTIAL","TXT_OTP","INDIA_CREDENTIAL"})
    if credential and (families["url"] or families["brand"]): raw += 10
    if "TXT_ACCOUNT_THREAT" in ids and (credential or "TXT_PAYMENT" in ids): raw += 8
    if len([name for name,values in families.items() if values and name!="privacy"]) == 1: raw *= .82
    if ml_probability is not None and ml_probability < .25 and raw < 28:
        raw *= .78
    return max(0, min(100, round(raw)))


def explain(score: int, category: str, signals: list[dict]) -> str:
    meaningful = sorted((s for s in signals if s["contribution"] > 0), key=lambda s: s["contribution"], reverse=True)
    if not meaningful:
        return "No strong threat indicators were detected. This does not guarantee the content is safe; verify unexpected requests independently."
    primary = meaningful[0]
    secondary = meaningful[1:3]
    statement = f"This content was rated {severity_for(score)} risk. Primary evidence: {primary['description']}"
    if primary.get("evidence"):
        statement += f" Detected evidence: “{primary['evidence']}”."
    if secondary:
        statement += " Supporting evidence includes " + " and ".join(item["name"].lower() for item in secondary) + "."
    return statement + " This evidence-based assessment indicates risk; it does not prove malicious intent."


def recommendations(score: int, signals: list[dict]) -> list[str]:
    ids = {s["id"] for s in signals}
    actions = ["Verify the sender or destination through a trusted, independent channel."]
    if any(i.startswith("URL_") for i in ids): actions.insert(0, "Do not open the link; use the organization’s official app or type its known address manually.")
    if {"TXT_CREDENTIAL", "TXT_OTP"} & ids: actions.append("Do not enter or share passwords, PINs, or one-time codes.")
    if "TXT_PAYMENT" in ids: actions.append("Pause any payment and confirm the request directly with the person or institution.")
    if score >= 75: actions.append("If you already acted, change affected credentials and contact the relevant institution immediately.")
    return actions[:4]
