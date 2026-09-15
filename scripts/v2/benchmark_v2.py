"""Unified current-machine benchmark; no result is a Snapdragon measurement."""
from __future__ import annotations
import importlib.metadata
import json
from pathlib import Path
import platform
import statistics
import subprocess
import sys
import time

import cv2
import numpy as np
import psutil

ROOT=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(ROOT))
from backend.app.adaptive import route
from backend.app.deep_guard import get_deep_guard
from backend.app.evidence_graph import build_graph
from backend.app.live_shield import LiveShield
from backend.app.model_runtime import get_classifier
from backend.app.ocr_engine import extract_text
from backend.app.orchestrator import analyze_text_full
from backend.app.url_analyzer import analyze_url

SAMPLE="SBI account suspended. Verify your password and OTP at hxxp://sbi-update[.]example/login immediately."

def summarize(values,warmup):
    measured=values[warmup:]
    return {"warmup":warmup,"repetitions":len(measured),"median_ms":statistics.median(measured),"mean_ms":statistics.mean(measured),"p95_ms":float(np.percentile(measured,95)),"min_ms":min(measured),"max_ms":max(measured)}

def measure(fn,repetitions=30,warmup=5):
    values=[]
    for _ in range(repetitions+warmup):
        began=time.perf_counter(); fn(); values.append((time.perf_counter()-began)*1000)
    return summarize(values,warmup)

def main():
    fast=get_classifier(); deep=get_deep_guard(); image_bytes=(ROOT/"data/samples/demo_multimodal.png").read_bytes()
    decoded=cv2.imdecode(np.frombuffer(image_bytes,np.uint8),cv2.IMREAD_COLOR); qr=cv2.QRCodeDetector()
    ocr_cache={}
    def do_ocr(): ocr_cache["value"]=extract_text(image_bytes)
    def do_qr(): qr.detectAndDecodeMulti(decoded)
    do_ocr(); do_qr()
    base={"input_type":"text","severity":"high","risk_score":80,"detected_urls":["http://sbi-update.example/login"],"signals":[{"id":"TXT_OTP","name":"OTP request","description":"credential","contribution":20,"evidence":"OTP"}],"details":{"routing":{"path":"deep","reasons":["test"]}}}
    clock=[0.0]; live=LiveShield(analyzer=lambda text,save: analyze_text_full(text,False),clock=lambda:clock[0]); live.start(start_thread=False)
    live_counter=[0]
    def do_live():
        live_counter[0]+=1; clock[0]+=4; live.process(SAMPLE+str(live_counter[0]))
    cold=[]
    for _ in range(5):
        began=time.perf_counter(); subprocess.run([sys.executable,"-c","from backend.app.main import app"],cwd=ROOT,check=True,capture_output=True); cold.append((time.perf_counter()-began)*1000)
    operations={
        "cold_backend_import":summarize(cold,0),
        "fast_guard":measure(lambda:fast.predict(SAMPLE),100,10),
        "deep_guard_total":measure(lambda:deep.predict(SAMPLE),50,5),
        "adaptive_decision":measure(lambda:route(.31,[{"id":"TXT_OTP","contribution":20}]),500,20),
        "url_engine":measure(lambda:analyze_url("http://sbi-update.example:8080/login"),100,10),
        "evidence_graph":measure(lambda:build_graph(base,[{"kind":"TextEvidence","label":"Submitted text","text":SAMPLE}]),100,10),
        "full_text_pipeline":measure(lambda:analyze_text_full(SAMPLE,False),30,5),
        "qr_decode":measure(do_qr,10,2),
        "ocr":measure(do_ocr,5,1),
        "multimodal_fusion":measure(lambda:analyze_text_full(ocr_cache["value"]["text"],False,{"input_type":"image","ocr_confidence":ocr_cache["value"].get("confidence"),"sources":[{"kind":"OCRText","label":"OCR text","text":ocr_cache["value"]["text"]}]}),10,2),
        "live_shield":measure(do_live,10,2),
    }
    live.stop()
    report={"schema_version":"1.0","measured":True,"measurement_scope":"Current AMD64 development PC only; not Snapdragon",
            "hardware":{"os":platform.platform(),"architecture":platform.machine(),"cpu":platform.processor(),"logical_cpus":psutil.cpu_count(),"ram_gib":round(psutil.virtual_memory().total/2**30,2)},
            "providers":{"fast_guard":fast.provider,"deep_guard":deep.provider},
            "versions":{name:importlib.metadata.version(name) for name in ("onnxruntime","numpy","scikit-learn","opencv-python","rapidocr-onnxruntime")},
            "operations":operations}
    out=ROOT/"reports/v2/unified_benchmarks.json"; out.write_text(json.dumps(report,indent=2),encoding="utf-8"); print(json.dumps(report,indent=2))

if __name__=="__main__": main()
