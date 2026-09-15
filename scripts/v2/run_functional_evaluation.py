"""Run curated adversarial/India scenarios through the real local pipeline."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from backend.app.orchestrator import analyze_text_full, analyze_url_full

def main():
    source=ROOT/"data/evaluation/v2_functional_cases.json"
    cases=json.loads(source.read_text(encoding="utf-8")); results=[]
    for case in cases:
        try:
            result=analyze_url_full(case["text"],False) if case["kind"]=="url" else analyze_text_full(case["text"],False)
            ids={s["id"] for s in result["signals"]}; checks=[]
            if "required_signal" in case: checks.append(case["required_signal"] in ids)
            if "absent_signal" in case: checks.append(case["absent_signal"] not in ids)
            if "min_risk" in case: checks.append(result["risk_score"]>=case["min_risk"])
            if "max_risk" in case: checks.append(result["risk_score"]<=case["max_risk"])
            passed=all(checks)
            results.append({"id":case["id"],"passed":passed,"risk_score":result["risk_score"],"severity":result["severity"],
                            "signals":sorted(ids),"route":result.get("details",{}).get("routing",{}).get("decision_class")})
        except Exception as exc:
            results.append({"id":case["id"],"passed":False,"error_type":type(exc).__name__,"error":str(exc)})
    report={"schema_version":"1.0","name":"India-focused multilingual and adversarial functional robustness evaluation",
            "not_classifier_accuracy":True,"cases":len(results),"passed":sum(r["passed"] for r in results),
            "failed":sum(not r["passed"] for r in results),"case_file_sha256":hashlib.sha256(source.read_bytes()).hexdigest(),"results":results}
    out=ROOT/"reports/v2/functional_evaluation.json"; out.parent.mkdir(parents=True,exist_ok=True); out.write_text(json.dumps(report,indent=2),encoding="utf-8")
    print(json.dumps(report,indent=2)); raise SystemExit(0 if report["failed"]==0 else 1)

if __name__=="__main__": main()
