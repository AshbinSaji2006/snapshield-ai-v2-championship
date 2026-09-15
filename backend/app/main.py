import io
import hashlib
import logging
import time
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI, File, HTTPException, Query, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.responses import JSONResponse
from fastapi.staticfiles import StaticFiles
from starlette.middleware.trustedhost import TrustedHostMiddleware
from PIL import Image, UnidentifiedImageError

from .config import ALLOWED_ORIGINS, MAX_IMAGE_BYTES, MAX_IMAGE_PIXELS, VERSION
from .database import clear_incidents, create_incident, delete_incident, get_incident, init_db, list_incidents, stats
from .orchestrator import analyze_text_full, analyze_url_full
from .model_runtime import get_classifier, model_status
from .ocr_engine import extract_text, ocr_status
from .runtime import runtime_manager
from .schemas import AnalysisResponse, TextRequest, URLRequest
from .deep_guard import get_deep_guard
from .live_shield import live_shield
from .evidence_graph import sanitized_export, build_graph
from pydantic import BaseModel

logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(name)s %(message)s")
logger = logging.getLogger("snapshield")


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    get_classifier()
    logger.info("SnapShield started provider=%s", runtime_manager.selected_provider)
    yield
    live_shield.stop()


app = FastAPI(title="SnapShield AI", version="2.0.0", lifespan=lifespan, docs_url="/api/docs", redoc_url=None)
app.add_middleware(CORSMiddleware, allow_origins=ALLOWED_ORIGINS, allow_credentials=False, allow_methods=["GET", "POST", "DELETE"], allow_headers=["Content-Type"])
app.add_middleware(TrustedHostMiddleware, allowed_hosts=["127.0.0.1", "localhost", "testserver"])


@app.middleware("http")
async def local_origin_and_security_headers(request, call_next):
    origin = request.headers.get("origin")
    if origin and origin not in ALLOWED_ORIGINS:
        return JSONResponse({"detail": "Cross-origin request blocked"}, status_code=403)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["Content-Security-Policy"] = "default-src 'self'; img-src 'self' blob: data:; style-src 'self' 'unsafe-inline'; script-src 'self'; connect-src 'self' http://127.0.0.1:8000 http://localhost:5173"
    return response


@app.get("/api/health")
def health():
    try:
        init_db(); database_status = "ready"
    except Exception:
        database_status = "error"
    return {"status": "ok" if database_status == "ready" else "degraded", "version": VERSION, "database_status": database_status, "model_status": model_status(), "runtime_provider": runtime_manager.selected_provider}


@app.get("/api/runtime")
def runtime():
    return runtime_manager.metadata() | {"ocr": ocr_status(), "model": model_status(), "deep_guard":get_deep_guard().status(), "live_shield":live_shield.status()}


@app.post("/api/analyze/text", response_model=AnalysisResponse)
def analyze_text(request: TextRequest): return analyze_text_full(request.text, request.save_incident)


@app.post("/api/analyze/url", response_model=AnalysisResponse)
def analyze_url_endpoint(request: URLRequest):
    try: return analyze_url_full(request.url, request.save_incident)
    except ValueError as exc: raise HTTPException(422, str(exc)) from exc


@app.post("/api/analyze/image", response_model=AnalysisResponse)
async def analyze_image(file: UploadFile = File(...), save_incident: bool = Query(True)):
    start = time.perf_counter()
    if file.content_type and file.content_type not in {"image/png", "image/jpeg", "image/webp", "application/octet-stream"}:
        raise HTTPException(415, "Upload MIME type must be PNG, JPEG, or WEBP")
    content = await file.read(MAX_IMAGE_BYTES + 1)
    if len(content) > MAX_IMAGE_BYTES: raise HTTPException(413, "Image exceeds the 10 MB limit")
    try:
        image = Image.open(io.BytesIO(content)); width, height = image.size; image.verify()
    except (UnidentifiedImageError, OSError, Image.DecompressionBombError) as exc:
        raise HTTPException(422, "The upload is not a valid decodable image") from exc
    allowed = {"PNG", "JPEG", "WEBP"}
    if image.format not in allowed: raise HTTPException(415, "Supported image formats: PNG, JPEG, WEBP")
    if width * height > MAX_IMAGE_PIXELS: raise HTTPException(413, "Image exceeds the 25-megapixel decoded-pixel limit")
    text = ""
    ocr = {"engine": "unavailable", "available": False, "text": "", "characters": 0, "line_count": 0, "confidence": None}
    qr_values: list[str] = []
    try:
        import cv2
        import numpy as np
        decoded = cv2.imdecode(np.frombuffer(content, dtype=np.uint8), cv2.IMREAD_COLOR)
        if decoded is not None:
            detector = cv2.QRCodeDetector()
            try:
                found, values, _, _ = detector.detectAndDecodeMulti(decoded)
                if found:
                    qr_values = [value for value in values if value]
            except (cv2.error, ValueError):
                value, _, _ = detector.detectAndDecode(decoded)
                if value:
                    qr_values = [value]
    except Exception:
        logger.warning("Local QR adapter unavailable or could not decode upload")
    try:
        ocr = extract_text(content); text = ocr["text"]
    except Exception as exc:
        logger.warning("Local OCR failed error=%s", type(exc).__name__)
    combined = "\n".join(part for part in [text, *qr_values] if part)
    if combined:
        sources = ([{"kind":"OCRText","label":"OCR-extracted text","text":text,"confidence":ocr.get("confidence")}] if text else []) + [{"kind":"QRPayload","label":f"QR payload {i+1}","text":value} for i,value in enumerate(qr_values)]
        result = analyze_text_full(combined, False, {"input_type":"image","qr":bool(qr_values),"ocr_confidence":ocr.get("confidence"),"sources":sources})
        result["input_type"] = "image"
        result["details"]["ocr"] = ocr
        result["details"]["qr"] = {"decoder": "OpenCV QRCodeDetector (local)", "count": len(qr_values), "contents": qr_values, "types": ["url" if value.lower().startswith(("http://", "https://")) else "wifi" if value.upper().startswith("WIFI:") else "payment" if value.lower().startswith(("bitcoin:", "ethereum:")) else "text" for value in qr_values]}
    else:
        result = analyze_text_full("Image contained no locally extractable text.", False)
        result.update({"input_type": "image", "risk_score": 0, "severity": "low", "threat_category": "No text extracted", "classification": "undetermined", "signals": [], "explanation": "The image was validated, but no OCR engine is available or no text could be extracted. No safety conclusion was made.", "recommendations": ["Review the image manually; image validity does not imply content safety."], "privacy_status": "Image decoded locally; source image not persisted"})
        result["details"]["ocr"] = ocr
        result["details"]["qr"] = {"decoder": "OpenCV QRCodeDetector (local)", "count": 0, "contents": [], "types": []}
        result["details"]["evidence_graph"] = build_graph(result,[])
    result["processing_time_ms"] = round((time.perf_counter() - start) * 1000, 2)
    if save_incident:
        result["id"] = create_incident(result, hashlib.sha256(content).hexdigest())
    return result


@app.get("/api/incidents")
def incidents(limit: int = Query(100, ge=1, le=500)): return list_incidents(limit)


@app.get("/api/incidents/{incident_id}")
def incident(incident_id: str):
    item = get_incident(incident_id)
    if item is None: raise HTTPException(404, "Incident not found")
    return item


@app.get("/api/incidents/{incident_id}/export")
def export_incident(incident_id: str):
    item=get_incident(incident_id)
    if item is None: raise HTTPException(404,"Incident not found")
    return JSONResponse(sanitized_export(item),headers={"Content-Disposition":"attachment; filename=snapshield-incident.json"})


class LiveConsent(BaseModel):
    enabled: bool
    consent: bool = False


@app.get("/api/live/status")
def live_status(): return live_shield.status()


@app.post("/api/live/control")
def live_control(request: LiveConsent):
    if request.enabled:
        if not request.consent: raise HTTPException(422,"Explicit clipboard monitoring consent is required")
        if not live_shield.status()["available"]: raise HTTPException(409,"Windows clipboard is unavailable")
        live_shield.start()
    else: live_shield.stop()
    return live_shield.status()


@app.get("/api/live/latest")
def live_latest(): return live_shield.latest()


@app.post("/api/live/ignore")
def live_ignore():
    live_shield.ignore(); return {"ignored":True}


@app.post("/api/live/save")
def live_save():
    identifier=live_shield.save()
    if identifier is None: raise HTTPException(404,"No current clipboard alert to save")
    return {"id":identifier}


@app.delete("/api/incidents/{incident_id}")
def remove_incident(incident_id: str):
    if not delete_incident(incident_id): raise HTTPException(404, "Incident not found")
    return {"deleted": True}


@app.delete("/api/incidents")
def remove_incidents(): return {"deleted": clear_incidents()}


@app.get("/api/stats")
def statistics(): return stats()


@app.post("/api/benchmark")
def benchmark(iterations: int = Query(25, ge=5, le=200)):
    sample = "Your account is suspended. Verify your password immediately at http://paypa1-secure.example/login"
    timings = []
    for _ in range(iterations):
        started = time.perf_counter(); analyze_text_full(sample, False); timings.append((time.perf_counter() - started) * 1000)
    timings.sort()
    return {"measured": True, "workload": "bundled phishing text through full local pipeline", "iterations": iterations, "provider": runtime_manager.selected_provider, "min_ms": round(timings[0], 2), "median_ms": round(timings[len(timings)//2], 2), "p95_ms": round(timings[min(len(timings)-1, int(len(timings)*.95))], 2), "max_ms": round(timings[-1], 2), "note": "Current-machine measurement; not a Snapdragon claim."}


DIST = Path(__file__).resolve().parents[2] / "frontend" / "dist"
DEMO_DIR = Path(__file__).resolve().parents[2] / "data" / "samples"
DEMO_ASSETS = {name: DEMO_DIR / name for name in ("demo_screenshot.png", "demo_multimodal.png", "demo_qr.png")}


@app.get("/api/demo/assets/{name}")
def demo_asset(name: str):
    target = DEMO_ASSETS.get(name)
    if target is None or not target.is_file():
        raise HTTPException(404, "Demo asset not found")
    return FileResponse(target)


if DIST.exists():
    app.mount("/assets", StaticFiles(directory=DIST / "assets"), name="assets")
    @app.get("/{path:path}")
    def spa(path: str):
        # Never turn an unknown or normalized API path into a successful SPA response.
        if path == "api" or path.startswith("api/"):
            raise HTTPException(404, "API route not found")
        root = DIST.resolve()
        target = (DIST / path).resolve()
        safe_target = target if target.is_relative_to(root) and target.is_file() else root / "index.html"
        return FileResponse(safe_target)
