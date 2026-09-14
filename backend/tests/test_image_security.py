import io
from pathlib import Path

from fastapi.testclient import TestClient
from PIL import Image

from backend.app.main import app


def test_operational_ocr_and_qr_multimodal_pipeline():
    path = Path("data/samples/demo_multimodal.png")
    with TestClient(app) as client:
        response = client.post("/api/analyze/image?save_incident=false", files={"file": (path.name, path.read_bytes(), "image/png")})
    body = response.json()
    assert response.status_code == 200 and body["details"]["ocr"]["confidence"] > .8
    assert body["details"]["qr"]["count"] == 1 and body["risk_score"] >= 75


def test_low_resolution_ocr_extracts_security_context():
    path = Path("data/samples/demo_low_resolution.jpg")
    with TestClient(app) as client:
        response = client.post("/api/analyze/image?save_incident=false", files={"file": (path.name, path.read_bytes(), "image/jpeg")})
    body = response.json()
    assert response.status_code == 200
    assert "account" in body["details"]["ocr"]["text"].lower()


def test_invalid_image_rejected():
    with TestClient(app) as client:
        assert client.post("/api/analyze/image", files={"file": ("bad.png", b"not an image", "image/png")}).status_code == 422


def test_wrong_mime_rejected():
    image = io.BytesIO(); Image.new("RGB", (10,10)).save(image, "PNG")
    with TestClient(app) as client:
        assert client.post("/api/analyze/image", files={"file": ("bad.txt", image.getvalue(), "text/plain")}).status_code == 415


def test_pixel_limit_rejected(monkeypatch):
    import backend.app.main as main
    image = io.BytesIO(); Image.new("RGB", (20,20)).save(image, "PNG")
    monkeypatch.setattr(main, "MAX_IMAGE_PIXELS", 100)
    with TestClient(app) as client:
        assert client.post("/api/analyze/image", files={"file": ("large.png", image.getvalue(), "image/png")}).status_code == 413


def test_unsupported_decoded_format_rejected():
    image = io.BytesIO(); Image.new("RGB", (20,20)).save(image, "BMP")
    with TestClient(app) as client:
        assert client.post("/api/analyze/image", files={"file": ("test.bmp", image.getvalue(), "application/octet-stream")}).status_code == 415
