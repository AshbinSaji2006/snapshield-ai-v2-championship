from __future__ import annotations

import re
from urllib.parse import urlsplit

from .url_analyzer import normalize_url
from .domain_intelligence import domain_facts, edit_distance

BRANDS: dict[str, dict[str, object]] = {
    "SBI": {"pattern": r"\b(?:SBI|State Bank of India)\b", "domains": ("sbi.co.in", "onlinesbi.sbi")},
    "Microsoft": {"pattern": r"\bMicrosoft\b", "domains": ("microsoft.com", "live.com", "office.com", "microsoftonline.com")},
    "Google": {"pattern": r"\bGoogle\b", "domains": ("google.com", "gmail.com")},
    "Apple": {"pattern": r"\bApple(?: ID)?\b", "domains": ("apple.com", "icloud.com")},
    "Amazon": {"pattern": r"\bAmazon\b", "domains": ("amazon.com", "amazon.in")},
    "PayPal": {"pattern": r"\bPayPal\b", "domains": ("paypal.com",)},
    "Netflix": {"pattern": r"\bNetflix\b", "domains": ("netflix.com",)},
    "Coinbase": {"pattern": r"\bCoinbase\b", "domains": ("coinbase.com",)},
}


def _matches(host: str, expected: tuple[str, ...]) -> bool:
    return any(host == domain or host.endswith("." + domain) for domain in expected)


def analyze_brand_mismatch(text: str, urls: list[str]) -> list[dict]:
    signals = []
    mentions = [(brand, info) for brand, info in BRANDS.items() if re.search(str(info["pattern"]), text, re.I)]
    for brand, info in mentions:
        expected = tuple(info["domains"])
        for raw in urls[:10]:
            try:
                host = urlsplit(normalize_url(raw)).hostname or ""
            except ValueError:
                continue
            if host and not _matches(host, expected):
                facts = domain_facts(host)
                token = facts["confusable_skeleton"].split(".")[-2] if "." in facts["confusable_skeleton"] else host
                signals.append({
                    "id": "BRAND_DOMAIN_MISMATCH", "name": f"{brand} domain mismatch", "severity": "high",
                    "description": f"The message references {brand}, but the destination does not match the finite official-domain map. Legitimate third-party services are possible; verify independently.",
                    "contribution": 24, "evidence": f"Observed {host}; expected {', '.join(expected)}", "brand": brand,
                    "observed_domain": host, "expected_domains": list(expected), "heuristic": True,
                    "registrable_domain": facts["registrable_domain"], "unicode_host": facts["unicode_host"],
                    "brand_edit_distance": edit_distance(token.casefold(), brand.casefold()),
                })
    return signals
