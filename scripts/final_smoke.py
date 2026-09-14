"""End-to-end source-build acceptance smoke test with only safe bundled inputs."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from fastapi.testclient import TestClient

from backend.app.main import app


def main() -> None:
    with TestClient(app) as client:
        health = client.get("/api/health")
        runtime = client.get("/api/runtime")
        ui = client.get("/")
        assert health.status_code == runtime.status_code == ui.status_code == 200
        before = client.get("/api/stats").json()["total_scans"]

        url = client.post("/api/analyze/url", json={"url": "http://192.0.2.1:8080/verify/login.exe", "save_incident": False})
        text = client.post("/api/analyze/text", json={"text": "URGENT: SBI account suspended. Verify password at http://paypa1-secure.example/login", "save_incident": False})
        pii = client.post("/api/analyze/text", json={"text": "Contact demo@example.com; password=not-a-real-secret", "save_incident": False})
        for response in (url, text, pii):
            assert response.status_code == 200
        assert "not-a-real-secret" not in pii.json()["redacted_text"]

        screenshot_path = ROOT / "data/samples/demo_multimodal.png"
        screenshot = client.post("/api/analyze/image?save_incident=false", files={"file": (screenshot_path.name, screenshot_path.read_bytes(), "image/png")})
        qr_path = ROOT / "data/samples/demo_qr.png"
        qr = client.post("/api/analyze/image?save_incident=false", files={"file": (qr_path.name, qr_path.read_bytes(), "image/png")})
        assert screenshot.status_code == qr.status_code == 200
        assert screenshot.json()["details"]["ocr"]["available"] is True
        assert screenshot.json()["details"]["qr"]["count"] == 1
        assert qr.json()["details"]["qr"]["count"] == 1

        created = client.post("/api/analyze/text", json={"text": "Safe smoke-test incident", "save_incident": True}).json()
        incident_id = created["id"]
        assert client.get(f"/api/incidents/{incident_id}").status_code == 200
        assert client.delete(f"/api/incidents/{incident_id}").json()["deleted"] is True
        after = client.get("/api/stats").json()["total_scans"]
        assert after == before

        report = {
            "health": health.json()["status"],
            "ui": "production SPA served",
            "provider": runtime.json()["selected_provider"],
            "url_score": url.json()["risk_score"],
            "text_score": text.json()["risk_score"],
            "pii_redacted": True,
            "ocr_lines": screenshot.json()["details"]["ocr"]["line_count"],
            "multimodal_qr_count": screenshot.json()["details"]["qr"]["count"],
            "qr_only_count": qr.json()["details"]["qr"]["count"],
            "incident_create_get_delete": True,
            "stats_restored": True,
        }
        print(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
