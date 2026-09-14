"""Unsigned Windows competition launcher for the local production application."""
from __future__ import annotations

import threading
import webbrowser
import os

import uvicorn

from backend.app.main import app


def main() -> None:
    url = "http://127.0.0.1:8765"
    if os.environ.get("SNAPSHIELD_NO_BROWSER") != "1":
        threading.Timer(1.2, lambda: webbrowser.open(url)).start()
    print("SnapShield AI - unsigned competition build")
    print(f"Local application: {url}")
    print("Press Ctrl+C to stop the local service.")
    uvicorn.run(app, host="127.0.0.1", port=8765, log_level="warning")


if __name__ == "__main__":
    main()
