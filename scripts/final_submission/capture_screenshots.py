"""Capture real SnapShield UI states through Chromium DevTools Protocol."""
from __future__ import annotations

import base64
import json
import os
import shutil
import subprocess
import tempfile
import time
import urllib.request
from pathlib import Path

import websocket
from PIL import Image


ROOT = Path(__file__).resolve().parents[2]
OUTPUT = ROOT / "docs" / "final_submission" / "assets" / "screenshots"
BASE_URL = "http://127.0.0.1:8765"
DEBUG_PORT = 9327
EDGE = Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe")
APP = ROOT / "release" / "SnapShieldAI" / "SnapShieldAI.exe"
WIDTH = 1920
HEIGHT = 1080


class CDP:
    def __init__(self, url: str):
        self.ws = websocket.create_connection(
            url, timeout=30, origin=f"http://127.0.0.1:{DEBUG_PORT}"
        )
        self.next_id = 0
        self.events: list[dict] = []

    def call(self, method: str, params: dict | None = None) -> dict:
        self.next_id += 1
        request_id = self.next_id
        self.ws.send(json.dumps({"id": request_id, "method": method, "params": params or {}}))
        while True:
            message = json.loads(self.ws.recv())
            if message.get("id") == request_id:
                if "error" in message:
                    raise RuntimeError(f"CDP {method}: {message['error']}")
                return message.get("result", {})
            self.events.append(message)

    def evaluate(self, expression: str):
        result = self.call(
            "Runtime.evaluate",
            {"expression": expression, "returnByValue": True, "awaitPromise": True},
        )
        if result.get("exceptionDetails"):
            raise RuntimeError(str(result["exceptionDetails"]))
        return result.get("result", {}).get("value")

    def close(self):
        self.ws.close()


def request_json(path: str, method: str = "GET") -> dict:
    request = urllib.request.Request(f"{BASE_URL}{path}", method=method)
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def wait_until(test, message: str, timeout: float = 35.0):
    deadline = time.time() + timeout
    while time.time() < deadline:
        try:
            value = test()
            if value:
                return value
        except Exception:
            pass
        time.sleep(0.2)
    raise TimeoutError(message)


def click_text(cdp: CDP, text: str):
    label = json.dumps(text)
    expression = f"""
      (() => {{
        const node = [...document.querySelectorAll('button')].find((button) =>
          (button.innerText || button.textContent || '').trim() === {label}
        );
        if (!node) return false;
        node.click();
        return true;
      }})()
    """
    if not cdp.evaluate(expression):
        raise RuntimeError(f"Button not found: {text}")


def wait_text(cdp: CDP, text: str, timeout: float = 35.0):
    label = json.dumps(text.lower())
    return wait_until(
        lambda: cdp.evaluate(f"document.body.innerText.toLowerCase().includes({label})"),
        f"Timed out waiting for text: {text}",
        timeout,
    )


def capture(cdp: CDP, filename: str, manifest: dict):
    cdp.evaluate("window.scrollTo(0, 0); document.activeElement?.blur(); true")
    time.sleep(1.25)
    result = cdp.call(
        "Page.captureScreenshot",
        {"format": "png", "fromSurface": True, "captureBeyondViewport": False},
    )
    path = OUTPUT / filename
    path.write_bytes(base64.b64decode(result["data"]))
    with Image.open(path) as image:
        if image.size != (WIDTH, HEIGHT):
            raise RuntimeError(f"Unexpected dimensions for {filename}: {image.size}")
    manifest[filename] = {
        "width": WIDTH,
        "height": HEIGHT,
        "source": BASE_URL,
        "captured_from_real_application": True,
    }


def analyze(cdp: CDP, demo_label: str, filename: str, manifest: dict, timeout: float = 35.0):
    click_text(cdp, demo_label)
    if demo_label in {"Screenshot", "QR"}:
        expected_file = "demo_multimodal.png" if demo_label == "Screenshot" else "demo_qr.png"
        wait_until(
            lambda: cdp.evaluate(
                f"document.querySelector('.dropzone strong')?.innerText === {json.dumps(expected_file)}"
            ),
            f"Bundled image did not load: {expected_file}",
            timeout,
        )
    click_text(cdp, "Analyze locally")
    wait_text(cdp, "Assessment complete", timeout)
    wait_until(
        lambda: not cdp.evaluate("document.body.innerText.includes('Analyzing…')"),
        "Analysis did not settle",
        timeout,
    )
    time.sleep(0.75)
    capture(cdp, filename, manifest)


def main():
    if not EDGE.exists():
        raise FileNotFoundError(EDGE)
    if not APP.exists():
        raise FileNotFoundError(APP)
    app_process = None
    try:
        health = request_json("/api/health")
    except Exception:
        app_environment = os.environ.copy()
        app_environment["SNAPSHIELD_NO_BROWSER"] = "1"
        app_process = subprocess.Popen(
            [str(APP)],
            cwd=ROOT,
            env=app_environment,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        health = wait_until(
            lambda: request_json("/api/health"),
            "Packaged SnapShield service did not start",
            45,
        )
    if health.get("status") != "ok":
        raise RuntimeError(f"Application is not healthy: {health}")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    profile = Path(tempfile.mkdtemp(prefix="snapshield-final-edge-"))
    os.environ["NO_PROXY"] = "127.0.0.1,localhost"
    process = subprocess.Popen(
        [
            str(EDGE),
            "--headless=new",
            f"--remote-debugging-port={DEBUG_PORT}",
            "--remote-allow-origins=*",
            f"--user-data-dir={profile}",
            f"--window-size={WIDTH},{HEIGHT}",
            "--force-device-scale-factor=1",
            "--hide-scrollbars",
            "--disable-gpu",
            "--disable-extensions",
            "--disable-background-networking",
            "--disable-component-update",
            "--disable-sync",
            "--no-proxy-server",
            "--metrics-recording-only",
            "--no-first-run",
            "--no-default-browser-check",
            BASE_URL,
        ],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    cdp = None
    manifest: dict[str, dict] = {}
    try:
        def page_target():
            with urllib.request.urlopen(
                f"http://127.0.0.1:{DEBUG_PORT}/json", timeout=2
            ) as response:
                targets = json.loads(response.read().decode("utf-8"))
            return next(
                (
                    item
                    for item in targets
                    if item.get("type") == "page" and BASE_URL in item.get("url", "")
                ),
                None,
            )

        target = wait_until(page_target, "Edge DevTools target did not start", 30)
        cdp = CDP(target["webSocketDebuggerUrl"])
        cdp.call("Page.enable")
        cdp.call("Runtime.enable")
        cdp.call("Log.enable")
        cdp.call(
            "Emulation.setDeviceMetricsOverride",
            {"width": WIDTH, "height": HEIGHT, "deviceScaleFactor": 1, "mobile": False},
        )
        cdp.call("Page.navigate", {"url": BASE_URL})
        wait_until(
            lambda: cdp.evaluate("document.readyState === 'complete'"),
            "Application page did not finish loading",
            30,
        )
        wait_text(cdp, "Local AI", 30)
        wait_text(cdp, "CPUExecutionProvider", 30)
        cdp.evaluate("document.documentElement.style.scrollBehavior='auto'; true")

        click_text(cdp, "Presentation mode")
        wait_text(cdp, "Exit presentation")
        click_text(cdp, "Analyze")
        wait_text(cdp, "Analyze suspicious content")

        analyze(cdp, "Legitimate", "02_legitimate_analysis.png", manifest)
        analyze(cdp, "Bank phish", "03_phishing_analysis.png", manifest)
        analyze(cdp, "Screenshot", "04_multimodal_screenshot_analysis.png", manifest, 45)
        wait_text(cdp, "Multimodal extraction")
        capture(cdp, "04_multimodal_screenshot_analysis.png", manifest)
        analyze(cdp, "QR", "05_qr_analysis.png", manifest, 45)
        wait_text(cdp, "QR decoded locally")
        capture(cdp, "05_qr_analysis.png", manifest)
        analyze(cdp, "PII guard", "06_pii_redaction.png", manifest)
        wait_text(cdp, "Sensitive data")
        capture(cdp, "06_pii_redaction.png", manifest)

        click_text(cdp, "Incident center")
        wait_text(cdp, "Local history")
        wait_until(
            lambda: cdp.evaluate("document.querySelectorAll('.incident-main').length >= 5"),
            "Expected demo incident history",
        )
        cdp.evaluate("document.querySelector('.incident-main')?.click(); true")
        wait_text(cdp, "Sanitized forensic record")
        capture(cdp, "07_incident_analytics.png", manifest)

        click_text(cdp, "Runtime")
        wait_text(cdp, "CPUExecutionProvider")
        click_text(cdp, "Run")
        wait_until(
            lambda: cdp.evaluate("!!document.querySelector('.bench-grid')"),
            "Runtime benchmark did not finish",
            45,
        )
        capture(cdp, "08_runtime_benchmarks.png", manifest)

        click_text(cdp, "Overview")
        wait_text(cdp, "Your data never needs to leave your device")
        wait_until(
            lambda: not cdp.evaluate("document.body.innerText.includes('Local scans\\n—')"),
            "Overview statistics did not load",
        )
        capture(cdp, "01_snapshield_dashboard.png", manifest)

        runtime = request_json("/api/runtime")
        manifest["runtime"] = {
            "selected_provider": runtime["selected_provider"],
            "snapdragon_npu_verified": runtime["snapdragon_npu_verified"],
        }
        (OUTPUT / "capture_manifest.json").write_text(
            json.dumps(manifest, indent=2), encoding="utf-8"
        )
        print(json.dumps(manifest, indent=2))
    finally:
        if cdp is not None:
            cdp.close()
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
        shutil.rmtree(profile, ignore_errors=True)
        if app_process is not None:
            app_process.terminate()
            try:
                app_process.wait(timeout=10)
            except subprocess.TimeoutExpired:
                app_process.kill()


if __name__ == "__main__":
    main()
