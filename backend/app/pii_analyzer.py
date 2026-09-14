import re
from typing import Any

PATTERNS = {
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "bearer_token": re.compile(r"(?i)\bBearer\s+[A-Za-z0-9._~+/-]{12,}"),
    "jwt": re.compile(r"\beyJ[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\.[A-Za-z0-9_-]{8,}\b"),
    "api_key": re.compile(r"(?i)\b(?:api[_-]?key|access[_-]?token)\s*[:=]\s*['\"]?([A-Za-z0-9_\-]{16,})"),
    "password": re.compile(r"(?i)\b(?:password|passwd|pwd)\s*[:=]\s*\S+"),
    "email": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
    "phone": re.compile(r"(?<!\w)(?:\+?\d[\d .()-]{7,}\d)(?!\w)"),
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "payment_card": re.compile(r"(?<!\d)(?:\d[ -]*?){13,19}(?!\d)"),
}


def _luhn(value: str) -> bool:
    digits = [int(c) for c in value if c.isdigit()]
    if not 13 <= len(digits) <= 19:
        return False
    total = 0
    parity = len(digits) % 2
    for index, digit in enumerate(digits):
        if index % 2 == parity:
            digit *= 2
            if digit > 9:
                digit -= 9
        total += digit
    return total % 10 == 0


def _mask(kind: str, value: str) -> str:
    if kind == "email":
        local, domain = value.split("@", 1)
        return local[:1] + "*****@" + domain
    if kind == "phone":
        return "*" * max(0, len(value) - 4) + value[-4:]
    if kind == "payment_card":
        digits = re.sub(r"\D", "", value)
        return "•••• •••• •••• " + digits[-4:]
    if kind == "private_key":
        return "[PRIVATE KEY REDACTED]"
    return value[: min(7, len(value))] + "********"


def analyze_pii(text: str) -> tuple[list[dict[str, Any]], str]:
    findings: list[dict[str, Any]] = []
    matches: list[tuple[int, int, str]] = []
    for kind, pattern in PATTERNS.items():
        for match in pattern.finditer(text):
            value = match.group(0)
            if kind == "payment_card" and not _luhn(value):
                continue
            masked = _mask(kind, value)
            findings.append({"type": kind, "masked_value": masked, "start": match.start(), "end": match.end(), "confidence": "high" if kind in {"private_key", "jwt", "email"} else "moderate", "risk_note": "Potentially sensitive; avoid sharing unnecessarily."})
            matches.append((match.start(), match.end(), masked))
    redacted = text
    for start, end, masked in sorted(matches, reverse=True):
        redacted = redacted[:start] + masked + redacted[end:]
    return findings, redacted

