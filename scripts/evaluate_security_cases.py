"""Evaluate curated adversarial and legitimate cases through the complete text pipeline."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from backend.app.orchestrator import analyze_text_full


def main() -> None:
    cases = json.loads((ROOT / "ml" / "evaluation" / "adversarial_cases.json").read_text(encoding="utf-8"))
    results = []
    for case in cases:
        analysis = analyze_text_full(case["text"], False)
        passed = analysis["risk_score"] >= case.get("expected_min", 0) and analysis["risk_score"] <= case.get("expected_max", 100)
        results.append({"id": case["id"], "label": case["label"], "score": analysis["risk_score"], "severity": analysis["severity"], "passed_expected_band": passed, "signals": [item["id"] for item in analysis["signals"]]})
    tp = sum(item["label"] == 1 and item["score"] >= 25 for item in results); fn = sum(item["label"] == 1 and item["score"] < 25 for item in results)
    tn = sum(item["label"] == 0 and item["score"] < 25 for item in results); fp = sum(item["label"] == 0 and item["score"] >= 25 for item in results)
    report = {"purpose": "curated functional/adversarial risk calibration; not model accuracy", "cases": len(results), "passed_expected_band": sum(item["passed_expected_band"] for item in results), "confusion_at_moderate_threshold": [[tn, fp], [fn, tp]], "false_positive_rate": fp / (fp + tn), "false_negative_rate": fn / (fn + tp), "results": results}
    output = ROOT / "ml" / "evaluation" / "results" / "adversarial_evaluation.json"; output.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    if report["passed_expected_band"] != report["cases"]: raise SystemExit(1)


if __name__ == "__main__": main()
