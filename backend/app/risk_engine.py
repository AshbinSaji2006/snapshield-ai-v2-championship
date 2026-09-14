from typing import Any


def severity_for(score: int) -> str:
    if score >= 75: return "critical"
    if score >= 50: return "high"
    if score >= 25: return "moderate"
    return "low"


def fuse(signals: list[dict[str, Any]], ml_probability: float | None = None) -> int:
    positive = [float(s["contribution"]) for s in signals if float(s["contribution"]) > 0]
    raw = sum(positive)
    # Require corroboration: diminishing returns avoid one weak feature dominating.
    if len(positive) == 1:
        raw *= 0.82
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
