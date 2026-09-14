# Installation

From source: install `requirements.txt`, run `npm install` and `npm run build` in `frontend`, then launch `python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000` from the repository root.

Prebuilt competition artifact: run `release/SnapShieldAI/SnapShieldAI.exe`; it opens <http://127.0.0.1:8765>. It is an AMD64, one-folder, unsigned competition build. Windows may display an unknown-publisher warning. See `DEPLOYMENT.md` for rebuild and Snapdragon ARM64 notes.
