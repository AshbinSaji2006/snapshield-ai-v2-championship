import os
import sys
from pathlib import Path

APP_NAME = "SnapShield AI"
VERSION = "1.0.0 Competition Build"
ROOT = Path(__file__).resolve().parents[2]
DATA_DIR = (Path(os.environ.get("LOCALAPPDATA", str(Path.home()))) / "SnapShieldAI") if getattr(sys, "frozen", False) else ROOT / "data"
DB_PATH = DATA_DIR / "snapshield.db"
MAX_TEXT_CHARS = 50_000
MAX_IMAGE_BYTES = 10 * 1024 * 1024
MAX_IMAGE_PIXELS = 25_000_000
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:8000",
    "http://127.0.0.1:8000",
    "http://localhost:8765",
    "http://127.0.0.1:8765",
]
