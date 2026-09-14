# Deployment

## Source production build

```powershell
python -m pip install -r requirements.txt
cd frontend
npm install
npm run build
cd ..
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000>. The backend serves the generated frontend bundle. Keep the loopback bind; exposing the service on a LAN would require authentication, TLS, rate limiting, and a broader threat review.

## Windows competition package

Build after the frontend bundle exists:

```powershell
python -m PyInstaller --noconfirm --clean --distpath release --workpath build SnapShieldAI.spec
```

Run `release/SnapShieldAI/SnapShieldAI.exe`. It starts a local service at `127.0.0.1:8765` and opens the default browser. Set `SNAPSHIELD_NO_BROWSER=1` for automation.

Verified artifact: AMD64 one-folder build, 372.28 MiB, 1,363 files. It is an **unsigned competition build**, not an installer. The package passed the real evaluator capture flow after the final visual-build fixes. Runtime data is written beneath `%LOCALAPPDATA%/SnapShieldAI`, not into the read-only bundle.

## Target Snapdragon build

The current artifact is AMD64 and is not a Snapdragon package. Rebuild in a native ARM64 Python environment with compatible ARM64 ONNX Runtime QNN/Windows ML, OpenCV, and OCR dependencies. Run the no-CPU-fallback procedure in [SNAPDRAGON.md](SNAPDRAGON.md) before describing it as NPU verified.

Production distribution additionally needs code signing, an installer/updater trust design, per-launch API authentication, and automated dependency/license scanning.
