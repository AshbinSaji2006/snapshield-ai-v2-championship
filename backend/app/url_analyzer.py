import ipaddress
import math
import re
from collections import Counter
from urllib.parse import parse_qs, unquote, urlsplit, urlunsplit

SHORTENERS = {"bit.ly", "tinyurl.com", "t.co", "goo.gl", "ow.ly", "is.gd", "cutt.ly", "rb.gy"}
SUSPICIOUS_WORDS = {"verify", "secure", "account", "update", "login", "signin", "wallet", "payment", "suspended", "confirm", "banking", "bonus", "gift"}
BRANDS = {"paypal", "microsoft", "google", "apple", "amazon", "netflix", "coinbase", "whatsapp", "facebook", "instagram", "bank"}
SAFE_BRAND_DOMAINS = {"paypal.com", "microsoft.com", "google.com", "apple.com", "amazon.com", "netflix.com", "coinbase.com", "whatsapp.com", "facebook.com", "instagram.com"}
BAD_EXTENSIONS = {".exe", ".scr", ".js", ".vbs", ".bat", ".cmd", ".msi", ".iso", ".zip"}


def _entropy(value: str) -> float:
    if not value:
        return 0.0
    return -sum((n / len(value)) * math.log2(n / len(value)) for n in Counter(value).values())


def normalize_url(raw: str) -> str:
    value = raw.strip()
    value = re.sub(r"(?i)^hxxps?\s*:\s*//", lambda match: "https://" if "hxxps" in match.group(0).lower() else "http://", value)
    value = value.replace("[.]", ".").replace("(.)", ".").replace("{.}", ".")
    if not re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*://", value):
        value = "https://" + value
    parts = urlsplit(value)
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), parts.path or "/", parts.query, ""))


def analyze_url(raw: str) -> dict:
    normalized = normalize_url(raw)
    parts = urlsplit(normalized)
    host = parts.hostname or ""
    if not host or parts.scheme not in {"http", "https"} or any(character.isspace() for character in host):
        raise ValueError("Enter a valid HTTP or HTTPS URL")
    signals = []

    def add(code: str, name: str, severity: str, description: str, points: int, evidence: str | None = None):
        signals.append({"id": code, "name": name, "severity": severity, "description": description, "contribution": points, "evidence": evidence})

    try:
        ipaddress.ip_address(host)
        add("URL_IP_HOST", "IP address host", "high", "Uses an IP address instead of a conventional domain.", 28, host)
    except ValueError:
        pass
    if parts.scheme == "http": add("URL_INSECURE_SCHEME", "Unencrypted scheme", "moderate", "Uses HTTP instead of HTTPS.", 10, "http://")
    if "xn--" in host: add("URL_PUNYCODE", "Punycode hostname", "high", "Internationalized hostname can conceal look-alike characters.", 20, host)
    if "@" in raw: add("URL_AT_SYMBOL", "Misleading @ symbol", "high", "An @ symbol can hide the true destination.", 22, "@")
    if raw.count("//") > 1: add("URL_DOUBLE_SLASH", "Extra double slash", "moderate", "Unexpected double slashes may obscure the URL structure.", 8)
    if len(normalized) > 120: add("URL_LENGTH", "Unusually long URL", "moderate", "The URL is unusually long.", 10, f"{len(normalized)} characters")
    if host.count(".") >= 4: add("URL_SUBDOMAINS", "Many subdomains", "moderate", "Many nested subdomains can disguise the registered domain.", 10, host)
    if host in SHORTENERS: add("URL_SHORTENER", "Shortened URL", "moderate", "A shortening service hides the final destination.", 14, host)
    if parts.port and parts.port not in {80, 443}: add("URL_PORT", "Unusual network port", "high", "Uses a non-standard web port.", 18, str(parts.port))
    if "%" in raw: add("URL_ENCODING", "Encoded characters", "low", "Encoded characters reduce readability.", 5)
    keywords = sorted(word for word in SUSPICIOUS_WORDS if word in unquote(normalized).lower())
    if keywords: add("URL_LURE_TERMS", "Credential or payment terms", "moderate", "Contains terms commonly used in account lures.", min(18, 5 + len(keywords) * 3), ", ".join(keywords))
    suffix = next((ext for ext in BAD_EXTENSIONS if parts.path.lower().endswith(ext)), None)
    if suffix: add("URL_FILE_TYPE", "Risky file extension", "high", "Points to a file type frequently used for payload delivery.", 24, suffix)
    brand_comparison = host.replace("1", "l").replace("0", "o")
    brand_hits = [brand for brand in BRANDS if brand in brand_comparison]
    if brand_hits and not any(host == d or host.endswith("." + d) for d in SAFE_BRAND_DOMAINS):
        add("URL_BRAND_MISMATCH", "Possible brand impersonation", "high", "A brand name appears outside its known primary domain.", 26, ", ".join(brand_hits))
    path_brand_hits = [brand for brand in BRANDS if brand in parts.path.lower() and brand not in host]
    if path_brand_hits:
        add("URL_BRAND_IN_PATH", "Brand name hidden in path", "moderate", "A brand appears in the path rather than the hostname; the hostname controls the destination.", 12, ", ".join(path_brand_hits))
    if host.count("-") >= 3: add("URL_HYPHENS", "Excessive hyphens", "low", "The hostname contains many hyphens.", 5, host)
    if sum(c.isdigit() for c in host) >= 6: add("URL_DIGITS", "Digit-heavy hostname", "low", "The hostname contains many digits.", 6, host)
    if _entropy(host.replace(".", "")) > 3.8 and len(host) > 18: add("URL_ENTROPY", "Random-looking hostname", "moderate", "Hostname has high character entropy.", 9, host)
    score = min(100, sum(int(s["contribution"]) for s in signals))
    return {"normalized_url": normalized, "host": host, "scheme": parts.scheme, "port": parts.port, "path_length": len(parts.path), "query_parameters": len(parse_qs(parts.query)), "signals": signals, "score": score}
