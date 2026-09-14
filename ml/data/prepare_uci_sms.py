"""Download, verify, deduplicate, and split the UCI SMS Spam Collection."""
from __future__ import annotations

import hashlib
import json
import re
import unicodedata
import urllib.request
import zipfile
from collections import Counter
from io import BytesIO
from pathlib import Path

from sklearn.model_selection import train_test_split

ROOT = Path(__file__).resolve().parents[2]
RAW_DIR = ROOT / "data" / "raw"
OUT_DIR = ROOT / "data" / "processed" / "uci_sms"
SOURCE_URL = "https://archive.ics.uci.edu/static/public/228/sms+spam+collection.zip"
SOURCE_PAGE = "https://archive.ics.uci.edu/dataset/228/sms+spam+collection"
EXPECTED_SHA256 = "1587ea43e58e82b14ff1f5425c88e17f8496bfcdb67a583dbff9eefaf9963ce3"
SEED = 42


def normalized_text(text: str) -> str:
    value = unicodedata.normalize("NFKC", text).casefold()
    return re.sub(r"\s+", " ", value).strip()


def near_fingerprint(text: str) -> str:
    value = normalized_text(text)
    value = re.sub(r"(?:https?://|www\.)\S+", " <url> ", value)
    value = re.sub(r"\b\d+(?:[.,]\d+)?\b", " <num> ", value)
    value = re.sub(r"[^a-z<> ]+", " ", value)
    return re.sub(r"\s+", " ", value).strip()


def download() -> bytes:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    destination = RAW_DIR / "sms_spam_collection.zip"
    if destination.exists():
        payload = destination.read_bytes()
    else:
        request = urllib.request.Request(SOURCE_URL, headers={"User-Agent": "SnapShield-AI-dataset-pipeline/1.0"})
        with urllib.request.urlopen(request, timeout=60) as response:
            payload = response.read()
        destination.write_bytes(payload)
    digest = hashlib.sha256(payload).hexdigest()
    if EXPECTED_SHA256 and digest != EXPECTED_SHA256:
        raise RuntimeError(f"Dataset checksum mismatch: {digest}")
    return payload


def load_rows(payload: bytes) -> list[tuple[int, str]]:
    with zipfile.ZipFile(BytesIO(payload)) as archive:
        member = next(name for name in archive.namelist() if name.rstrip("/").endswith("SMSSpamCollection"))
        content = archive.read(member).decode("utf-8")
    rows = []
    for line in content.splitlines():
        label, text = line.split("\t", 1)
        rows.append((1 if label == "spam" else 0, text.strip()))
    return rows


def deduplicate(rows: list[tuple[int, str]]) -> tuple[list[tuple[int, str]], dict[str, int]]:
    exact: dict[str, tuple[int, str]] = {}
    exact_removed = 0
    conflicts_removed = 0
    for label, text in rows:
        key = normalized_text(text)
        if key in exact:
            exact_removed += 1
            if exact[key][0] != label:
                exact[key] = (-1, text)
                conflicts_removed += 1
        else:
            exact[key] = (label, text)
    candidates = [row for row in exact.values() if row[0] >= 0]
    near: dict[str, tuple[int, str]] = {}
    near_removed = 0
    for label, text in candidates:
        key = near_fingerprint(text)
        if len(key) < 8:
            key = normalized_text(text)
        if key in near:
            near_removed += 1
            if near[key][0] != label:
                near[key] = (-1, text)
                conflicts_removed += 1
        else:
            near[key] = (label, text)
    retained = [row for row in near.values() if row[0] >= 0]
    return retained, {"exact_duplicates_removed": exact_removed, "near_duplicates_removed": near_removed, "label_conflicts_removed": conflicts_removed}


def write_split(name: str, rows: list[tuple[int, str]]) -> None:
    content = "label\ttext\n" + "\n".join(f"{label}\t{text.replace(chr(9), ' ').replace(chr(10), ' ')}" for label, text in rows) + "\n"
    (OUT_DIR / f"{name}.tsv").write_text(content, encoding="utf-8")


def main() -> None:
    payload = download()
    digest = hashlib.sha256(payload).hexdigest()
    original = load_rows(payload)
    clean, removal = deduplicate(original)
    labels = [row[0] for row in clean]
    train_val, test = train_test_split(clean, test_size=0.15, random_state=SEED, stratify=labels)
    train, validation = train_test_split(train_val, test_size=0.1764705882, random_state=SEED, stratify=[row[0] for row in train_val])
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    for name, rows in (("train", train), ("validation", validation), ("test", test)):
        write_split(name, rows)
    report = {
        "name": "SMS Spam Collection", "publisher": "UCI Machine Learning Repository",
        "doi": "10.24432/C5CC84", "source_page": SOURCE_PAGE, "download_url": SOURCE_URL,
        "license": "CC BY 4.0", "accessed": "2026-09-12", "sha256": digest,
        "original_rows": len(original), "retained_after_deduplication": len(clean), **removal,
        "split_seed": SEED, "split_strategy": "stratified 70/15/15 after exact and normalized near-duplicate removal",
        "splits": {name: {"rows": len(rows), "class_distribution": dict(Counter("spam" if label else "ham" for label, _ in rows))} for name, rows in (("train", train), ("validation", validation), ("test", test))},
    }
    (OUT_DIR / "dataset_manifest.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    (RAW_DIR / "ATTRIBUTION.md").write_text("# SMS Spam Collection\n\nAlmeida, T. & Hidalgo, J. (2011). SMS Spam Collection [Dataset]. UCI Machine Learning Repository. https://doi.org/10.24432/C5CC84\n\nLicense: Creative Commons Attribution 4.0 International.\n", encoding="utf-8")
    print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
