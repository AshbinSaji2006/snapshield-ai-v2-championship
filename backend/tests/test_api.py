from fastapi.testclient import TestClient
import io
import qrcode
from backend.app.main import app


def test_health_and_runtime():
    with TestClient(app) as client:
        health = client.get("/api/health")
        assert health.status_code == 200
        assert health.json()["database_status"] == "ready"
        runtime = client.get("/api/runtime").json()
        assert runtime["selected_provider"]
        assert isinstance(runtime["snapdragon_npu_verified"], bool)


def test_text_api_does_not_echo_source():
    secret = "password=never-log-me"
    with TestClient(app) as client:
        body = client.post("/api/analyze/text", json={"text": secret, "save_incident": False}).json()
        assert secret not in str(body)
        assert "never-log-me" not in body["redacted_text"].lower()


def test_rejects_bad_url():
    with TestClient(app) as client:
        assert client.post("/api/analyze/url", json={"url": "file:///etc/passwd"}).status_code == 422


def test_qr_image_uses_real_url_pipeline():
    image = qrcode.make("http://192.0.2.1:8080/verify/login.exe")
    content = io.BytesIO(); image.save(content, format="PNG")
    with TestClient(app) as client:
        response = client.post("/api/analyze/image?save_incident=false", files={"file": ("demo.png", content.getvalue(), "image/png")})
        assert response.status_code == 200
        body = response.json()
        assert body["details"]["qr"]["count"] == 1
        assert any(signal["id"] == "URL_IP_HOST" for signal in body["signals"])


def test_untrusted_browser_origin_is_blocked():
    with TestClient(app) as client:
        response = client.post("/api/analyze/text", headers={"Origin": "https://attacker.example"}, json={"text": "hello"})
        assert response.status_code == 403


def test_security_headers_are_present():
    with TestClient(app) as client:
        response = client.get("/api/runtime")
        assert response.headers["x-content-type-options"] == "nosniff"
        assert response.headers["content-security-policy"].startswith("default-src 'self'")


def test_demo_asset_route_is_allowlisted():
    with TestClient(app) as client:
        assert client.get("/api/demo/assets/demo_qr.png").status_code == 200
        assert client.get("/api/demo/assets/not_allowlisted.png").status_code == 404
        traversal = client.get("/api/demo/assets/%2e%2e/%2e%2e/README.md")
        assert "SnapShield AI" not in traversal.text or traversal.status_code == 404
