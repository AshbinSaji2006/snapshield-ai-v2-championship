"""Bounded security normalization; originals remain separate and are never persisted."""
from dataclasses import dataclass
import html
import re
import unicodedata
from urllib.parse import unquote

# Deliberately finite, auditable confusable subset. Not a complete Unicode skeleton.
CONFUSABLES = str.maketrans({"а":"a", "е":"e", "о":"o", "р":"p", "с":"c", "у":"y", "х":"x", "і":"i", "ј":"j", "ѕ":"s", "А":"A", "В":"B", "Е":"E", "К":"K", "М":"M", "Н":"H", "О":"O", "Р":"P", "С":"C", "Т":"T", "Х":"X", "Ι":"I", "Ο":"O", "ο":"o", "Ρ":"P"})

@dataclass(frozen=True)
class NormalizedEvidence:
    original_text: str
    normalized_security_text: str
    transformations: tuple[str, ...]
    script: str

def normalize_security(text: str) -> NormalizedEvidence:
    if len(text) > 50000:
        raise ValueError("Text exceeds the 50,000 character limit")
    original = text
    changes = []
    def stage(value, label):
        nonlocal text
        if value != text: changes.append(label)
        text = value
    stage(html.unescape(text), "HTML entities decoded")
    stage(unicodedata.normalize("NFKC", text), "Unicode NFKC")
    stage("".join(c for c in text if unicodedata.category(c) != "Cf"), "Invisible formatting characters removed")
    # Apply the finite skeleton only to tokens containing Latin, never all Cyrillic text.
    stage(re.sub(r"\w+", lambda m: m.group().translate(CONFUSABLES) if re.search("[A-Za-z]",m.group()) else m.group(), text), "Mixed-script confusables normalized")
    stage(re.sub(r"(?i)\bhxxp(s?)\s*:\s*/\s*/",r"http\1://",text), "Defanged URL scheme normalized")
    stage(re.sub(r"\s*[\[({]\s*\.\s*[\])}]\s*", ".", text), "Defanged domain separator normalized")
    stage(re.sub(r"(?i)\bhttps?%3a%2f%2f[^\s<>]+",lambda m:unquote(m.group()),text), "Encoded URL decoded once")
    stage(re.sub(r"(?i)\b(https?)\s*:\s*/\s*/\s*",r"\1://",text), "Spaced URL scheme normalized")
    stage(re.sub(r"(?i)(https?://[\w.-]{1,253})\s*\.\s*([a-z]{2,24})\b",r"\1.\2",text), "Spaced hostname normalized")
    stage(re.sub(r"(?i)\bp[\s.\-_]*a[\s.\-_]*s[\s.\-_]*s[\s.\-_]*w[\s.\-_]*o[\s.\-_]*r[\s.\-_]*d\b", "password", text), "Spaced credential word normalized")
    stage(re.sub(r"\s+"," ",text).strip(), "Whitespace normalized")
    devanagari = bool(re.search(r"[\u0900-\u097f]",original))
    latin = bool(re.search(r"[A-Za-z]",original))
    other = any(c.isalpha() and not ("LATIN" in unicodedata.name(c,"") or "DEVANAGARI" in unicodedata.name(c,"")) for c in original)
    other_remaining = any(c.isalpha() and not ("LATIN" in unicodedata.name(c,"") or "DEVANAGARI" in unicodedata.name(c,"")) for c in text)
    script = "mixed Latin/Devanagari" if devanagari and latin else "Devanagari" if devanagari else "other/unsupported script" if other_remaining else "Latin with normalized confusables" if other else "Latin or neutral (language not inferred)"
    return NormalizedEvidence(original,text,tuple(changes),script)

def normalization_signals(evidence):
    signals=[]
    for change in evidence.transformations:
        if change in {"Whitespace normalized", "Unicode NFKC"}: continue
        signals.append({"id":"NORM_"+str(evidence.transformations.index(change)),"name":change,
                        "severity":"moderate","description":"A separate normalized view was used for security checks; the source was preserved in memory.",
                        "contribution":7 if "URL" in change or "domain" in change else 5,"evidence":change})
    return signals
