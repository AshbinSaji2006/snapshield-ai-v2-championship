"""Assemble the reproducible v2 Championship handoff without publishing it."""
from __future__ import annotations

import hashlib
import json
import shutil
import zipfile
from datetime import datetime, timezone
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "release" / "v2_championship"
DOCS = ROOT / "docs" / "v2"
DIST = ROOT / "dist" / "SnapShieldAI"
DESKTOP_ZIP = OUT / "SnapShield_AI_v2_Desktop_AMD64_Unsigned.zip"
SUBMISSION_ZIP = OUT / "SnapShield_AI_v2_Championship_Submission.zip"


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def copy(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, destination)


def zip_tree(source: Path, destination: Path, prefix: str) -> None:
    with zipfile.ZipFile(destination, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(source.rglob("*")):
            if path.is_file():
                archive.write(path, Path(prefix) / path.relative_to(source))


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    if not (DIST / "SnapShieldAI.exe").exists():
        raise FileNotFoundError("Build dist/SnapShieldAI before assembling the release")

    document_names = [
        "PROJECT_SUMMARY.md",
        "MODEL_CARD.md",
        "FINAL_PRESENTER_SCRIPT.md",
        "FINAL_DEMO_VIDEO_SCRIPT.md",
        "PRESENTATION_SCRIPT_90SEC.md",
        "PRESENTATION_SCRIPT_3MIN.md",
        "JUDGE_QA_CHAMPIONSHIP.md",
        "TEST_REPORT.md",
        "CLAIM_LEDGER.md",
        "LIMITATIONS.md",
        "DATA_PROTOCOL.md",
        "DEEP_GUARD_MODEL_TOURNAMENT.md",
        "ADAPTIVE_ROUTING.md",
        "CROSS_DOMAIN_EVALUATION.md",
        "ADVERSARIAL_EVALUATION.md",
        "RISK_CALIBRATION.md",
        "RISK_FUSION.md",
        "THREAT_EVIDENCE_GRAPH.md",
        "LIVE_SHIELD.md",
        "SNAPDRAGON_DEPLOYMENT.md",
        "AI_HUB_HUMAN_HANDOFF.md",
        "ARM64_BUILD.md",
        "SECURITY_REVIEW.md",
        "PRIVACY_VERIFICATION.md",
        "PUBLIC_REPOSITORY_AUDIT.md",
        "PORTAL_ANSWERS.md",
        "FINAL_CHECKLIST.md",
        "FINAL_CLAIM_AUDIT.md",
        "REJECTED_FEATURES.md",
        "FINAL_SCORECARD.md",
        "V1_VS_V2_SCORECARD.md",
    ]
    for name in document_names:
        copy(DOCS / name, OUT / "documents" / name)

    copy(ROOT / "README.md", OUT / "documents" / "README.md")
    copy(ROOT / "DATASETS.md", OUT / "documents" / "DATASETS.md")
    copy(ROOT / "LICENSE", OUT / "documents" / "LICENSE")
    copy(ROOT / "THIRD_PARTY_NOTICES.md", OUT / "documents" / "THIRD_PARTY_NOTICES.md")
    copy(ROOT / "reports" / "snapdragon" / "SNAPDRAGON_VALIDATION_REPORT.md", OUT / "documents" / "SNAPDRAGON_VALIDATION_REPORT.md")

    for path in sorted((DOCS / "assets" / "screenshots").glob("*.png")):
        copy(path, OUT / "screenshots" / path.name)
    for path in sorted((DOCS / "assets" / "graphics").glob("*.png")):
        copy(path, OUT / "graphics" / path.name)
    for path in sorted((DOCS / "assets" / "slides").glob("*.PNG")):
        copy(path, OUT / "slide_proofs" / path.name)

    evidence = [
        "model_evaluation.json",
        "adaptive_routing_evaluation.json",
        "adaptive_routing_evaluation_v2.2.json",
        "functional_evaluation.json",
        "failure_analysis.json",
        "unified_benchmarks.json",
    ]
    for name in evidence:
        copy(ROOT / "reports" / "v2" / name, OUT / "evidence" / name)
    copy(ROOT / "ml" / "v2" / "deep_guard" / "manifest.json", OUT / "evidence" / "deep_guard_manifest.json")
    copy(ROOT / "ml" / "v2" / "router_policy.json", OUT / "evidence" / "router_policy.json")
    for name in ["model.onnx", "model.qdq.onnx", "tokenizer.json", "manifest.json"]:
        copy(ROOT / "ml" / "v2" / "deep_guard" / name, OUT / "models" / "deep_guard" / name)
    copy(ROOT / "ml" / "artifacts" / "text_classifier.onnx", OUT / "models" / "fast_guard" / "text_classifier.onnx")
    copy(ROOT / "ml" / "v2" / "fast_calibration.json", OUT / "models" / "fast_guard" / "fast_calibration.json")
    copy(DOCS / "FINAL_CLAIM_AUDIT.md", OUT / "FINAL_CLAIM_AUDIT.md")

    (OUT / "PUBLIC_REPOSITORY_URL_PENDING").write_text(
        "Replace only after the owner creates and verifies the public repository.\n", encoding="utf-8"
    )
    (OUT / "DEMO_VIDEO_PENDING").write_text(
        "A real 3–4 minute application recording requires human screen/cursor/narration capture. "
        "Use documents/FINAL_DEMO_VIDEO_SCRIPT.md.\n", encoding="utf-8"
    )
    (OUT / "RELEASE_README.md").write_text(
        "# SnapShield AI v2 Championship handoff\n\n"
        "Use the PDF for fixed-layout judging and the PPTX when an editable deck is accepted. "
        "The desktop archive is unsigned AMD64 and should be uploaded only if the portal accepts its size/type. "
        "The smaller Championship Submission ZIP intentionally excludes that desktop archive. "
        "QNN/Snapdragon NPU hardware validation and the real demo video remain pending.\n",
        encoding="utf-8",
    )

    newest_dist = max(path.stat().st_mtime for path in DIST.rglob("*") if path.is_file())
    if not DESKTOP_ZIP.exists() or DESKTOP_ZIP.stat().st_mtime < newest_dist:
        zip_tree(DIST, DESKTOP_ZIP, "SnapShieldAI")

    build_info = {
        "product": "SnapShield AI",
        "version": "2.0.0 Championship Candidate",
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "desktop": {"platform": "Windows AMD64", "signed": False, "smoke_tested": True},
        "verified_provider": "CPUExecutionProvider",
        "qnn_hardware_validation": "pending",
        "backend_tests": 100,
        "functional_checks": "20/20",
    }
    (OUT / "BUILD_INFO.json").write_text(json.dumps(build_info, indent=2) + "\n", encoding="utf-8")

    excluded = {"checksums.txt", "FINAL_RELEASE_CHECKSUMS.txt", SUBMISSION_ZIP.name}
    files = [p for p in sorted(OUT.rglob("*")) if p.is_file() and p.name not in excluded]
    checks = "\n".join(f"{sha256(path)}  {path.relative_to(OUT).as_posix()}" for path in files) + "\n"
    (OUT / "checksums.txt").write_text(checks, encoding="utf-8")

    with zipfile.ZipFile(SUBMISSION_ZIP, "w", zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(OUT.rglob("*")):
            if not path.is_file() or path in {SUBMISSION_ZIP, DESKTOP_ZIP}:
                continue
            archive.write(path, Path("SnapShield_AI_v2_Championship") / path.relative_to(OUT))

    important = [
        DIST / "SnapShieldAI.exe",
        OUT / "SnapShield_AI_v2_Championship_Presentation.pptx",
        OUT / "SnapShield_AI_v2_Championship_Presentation.pdf",
        DESKTOP_ZIP,
        SUBMISSION_ZIP,
    ]
    final = "\n".join(f"{sha256(path)}  {path.relative_to(ROOT).as_posix()}" for path in important) + "\n"
    (OUT / "FINAL_RELEASE_CHECKSUMS.txt").write_text(final, encoding="utf-8")
    print(json.dumps({"release": str(OUT), "files": len(files), "desktop_zip_bytes": DESKTOP_ZIP.stat().st_size,
                      "submission_zip_bytes": SUBMISSION_ZIP.stat().st_size}, indent=2))


if __name__ == "__main__":
    main()
