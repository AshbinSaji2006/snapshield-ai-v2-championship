"""Publisher-verified cross-dataset holdout with explicit UCI contamination removal."""
from pathlib import Path
import csv
import hashlib
import json
import re
import unicodedata
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

ROOT = Path(__file__).resolve().parents[2]

def key(text):
    text = unicodedata.normalize("NFKC", text).casefold()
    text = re.sub(r"https?://\S+|www\.\S+", " URL ", text)
    text = re.sub(r"\d+", " NUM ", text)
    return re.sub(r"\W+", " ", text).strip()

def main():
    source = ROOT / "data/raw/mendeley_sms/Dataset_5971.csv"
    raw = source.read_bytes()
    encoding = "utf-8-sig"
    try:
        raw.decode(encoding)
    except UnicodeDecodeError:
        encoding = "cp1252"
    rows = list(csv.DictReader(raw.decode(encoding).splitlines()))
    uci = []
    for name in ("train", "validation", "test"):
        uci += [r.split("\t", 1)[1] for r in (ROOT / f"data/processed/uci_sms/{name}.tsv").read_text(encoding="utf-8").splitlines()[1:]]
    uci_keys = {key(x) for x in uci}
    seen = {}
    excluded = []
    retained = []
    for i, row in enumerate(rows):
        text = row["TEXT"].strip()
        label = row["LABEL"].strip().lower()
        if label not in {"ham", "spam", "smishing"} or not text:
            excluded.append({"row": i, "reason": "invalid_label_or_empty"}); continue
        normalized = key(text)
        if normalized in uci_keys:
            excluded.append({"row": i, "reason": "uci_normalized_overlap"}); continue
        if normalized in seen:
            excluded.append({"row": i, "reason": "internal_normalized_duplicate"})
            if seen[normalized]["original_label"] != label:
                seen[normalized]["conflict"] = True
            continue
        item = {"source_row": i, "text": text, "label": int(label != "ham"), "original_label": label,
                "text_sha256": hashlib.sha256(text.encode()).hexdigest()}
        seen[normalized] = item; retained.append(item)
    clean = []
    for item in retained:
        if item.pop("conflict", False):
            excluded.append({"row": item["source_row"], "reason": "conflicting_labels"})
        else:
            clean.append(item)
    retained = clean
    vec = TfidfVectorizer(analyzer="char_wb", ngram_range=(3, 5), max_features=40000, dtype=np.float32)
    features = vec.fit_transform([key(x) for x in uci] + [key(x["text"]) for x in retained])
    reference = features[:len(uci)]
    clean = []
    for start in range(0, len(retained), 128):
        chunk = features[len(uci)+start:len(uci)+start+128]
        maxima = (chunk @ reference.T).max(axis=1).toarray().ravel()
        for item, similarity in zip(retained[start:start+128], maxima):
            if similarity >= .90:
                excluded.append({"row": item["source_row"], "reason": "uci_near_overlap", "similarity": float(similarity)})
            else:
                clean.append(item)
    # Internal near duplicates: fixed source order, no model-error-dependent removal.
    accepted = []
    if clean:
        matrix = vec.transform([key(x["text"]) for x in clean])
        for i, item in enumerate(clean):
            if accepted and float((matrix[i] @ matrix[accepted].T).max()) >= .90:
                excluded.append({"row": item["source_row"], "reason": "internal_near_duplicate"})
            else:
                accepted.append(i)
    final = [clean[i] for i in accepted]
    out = ROOT / "data/processed/cross_domain"
    out.mkdir(parents=True, exist_ok=True)
    target = out / "mendeley_holdout.json"
    target.write_text(json.dumps(final, ensure_ascii=False, indent=2), encoding="utf-8")
    report = {"role": "external holdout only; never train/select/tune", "source_csv_sha256": hashlib.sha256(raw).hexdigest(),
              "encoding": encoding, "original_count": len(rows), "retained_count": len(final),
              "retained_labels": {label: sum(x["original_label"] == label for x in final) for label in ("ham", "spam", "smishing")},
              "overlap_reference": "all UCI train, validation, test messages", "cosine_threshold": .90,
              "excluded": excluded, "holdout_sha256": hashlib.sha256(target.read_bytes()).hexdigest()}
    (out / "manifest.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps({k:v for k,v in report.items() if k != "excluded"}), flush=True)

if __name__ == "__main__":
    main()
