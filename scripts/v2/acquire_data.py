"""Download only the original licensed archive and pinned offline suffix list."""
from pathlib import Path
import hashlib
import json
import urllib.request
import datetime
import zipfile

ROOT = Path(__file__).resolve().parents[2]
ARCHIVE_URL = "https://data.mendeley.com/public-files/datasets/f45bkkt8pr/files/edb361de-918d-469f-9106-e84823830665/file_downloaded"
EXPECTED = "9bbf3188fdad81495d8e82825648b9b63b53fc86841a3d26c02629990b233cc3"

def fetch(url):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (SnapShield research download)"})
    with urllib.request.urlopen(req, timeout=60) as response:
        return response.read(10_000_001)

def main():
    out = ROOT / "data" / "raw" / "mendeley_sms"
    out.mkdir(parents=True, exist_ok=True)
    content = fetch(ARCHIVE_URL)
    if hashlib.sha256(content).hexdigest() != EXPECTED:
        raise ValueError("Publisher archive SHA-256 mismatch")
    archive = out / "Dataset_5971.zip"
    archive.write_bytes(content)
    with zipfile.ZipFile(archive) as zf:
        members = [{"name": z.filename, "bytes": z.file_size} for z in zf.infolist()]
        print(json.dumps(members), flush=True)
        for member in zf.infolist():
            if member.filename.lower().endswith(".csv") and member.file_size <= 5_000_000:
                # Copy CSV data by basename only; never execute the archive's scripts.
                (out / Path(member.filename).name).write_bytes(zf.read(member))
    manifest = {"source": ARCHIVE_URL, "canonical": "https://doi.org/10.17632/f45bkkt8pr.1",
                "authors": ["Sandhya Mishra", "Devpriya Soni"], "license": "CC-BY-4.0",
                "acquired_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
                "sha256": EXPECTED, "publisher_hash_verified": True, "archive_bytes": len(content),
                "members": members, "role": "cross-dataset evaluation only"}
    (out / "provenance.json").write_text(json.dumps(manifest, indent=2), encoding="utf-8")
    psl = fetch("https://publicsuffix.org/list/public_suffix_list.dat")
    if len(psl) > 2_000_000 or b"https://mozilla.org/MPL/2.0/" not in psl[:500]:
        raise ValueError("Unexpected PSL response")
    target = ROOT / "backend" / "resources"
    target.mkdir(parents=True, exist_ok=True)
    (target / "public_suffix_list.dat").write_bytes(psl)
    (target / "public_suffix_list.provenance.json").write_text(json.dumps({
        "source": "https://publicsuffix.org/list/public_suffix_list.dat", "license": "MPL-2.0",
        "acquired_utc": manifest["acquired_utc"], "sha256": hashlib.sha256(psl).hexdigest(),
        "runtime_network_refresh": False}, indent=2), encoding="utf-8")
    print("Original dataset hash verified; offline PSL acquired.", flush=True)

if __name__ == "__main__":
    main()
