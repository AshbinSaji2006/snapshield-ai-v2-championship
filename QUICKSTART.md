# SnapShield AI Quick Start

## Fastest path: verified Windows package

From the repository root, run:

```powershell
.\release\SnapShieldAI\SnapShieldAI.exe
```

The unsigned competition build starts a local service on `127.0.0.1:8765` and opens the application. A Windows reputation warning is possible because the executable is not code-signed. Do not bypass an organizational policy to run it.

Confirm the header shows **Local AI active**. Open **Runtime** to see the provider actually selected on that machine. Do not infer Snapdragon NPU use from the device name.

## Run from source

Requirements: Windows, Python 3.11+, and Node.js 20.19+ or 22.12+.

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
Set-Location frontend
npm ci
npm run build
Set-Location ..
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```

Open <http://127.0.0.1:8000>. No cloud API key is required.

## Run the safe demo

1. Open **Analyze**.
2. Select **Legitimate**, then **Analyze locally**.
3. Select **Bank phish**, then **Analyze locally**.
4. Select **Screenshot**, then **Analyze locally**.
5. Select **PII guard**, then **Analyze locally**.
6. Open **Runtime** and report the displayed provider exactly.

All built-in samples are synthetic and inert. The exact presenter narration is in [docs/final_submission/10_DEMO_SCRIPT.md](docs/final_submission/10_DEMO_SCRIPT.md).

## Verify the source build

```powershell
python -m pytest
Set-Location frontend
npm run lint
npm run typecheck
npm run build
```

The canonical facts and claim boundaries are in [SUBMISSION_FACTS.md](SUBMISSION_FACTS.md).

## Troubleshooting

- **Local AI offline:** wait five seconds, close the application, and relaunch once.
- **Port already in use:** stop the existing local SnapShield/Uvicorn process or choose the appropriate documented port for source mode.
- **Image result is slower:** OCR and QR decoding are heavier than text analysis; allow up to 20 seconds during a demo.
- **QNN unavailable:** CPU fallback is expected on non-compatible hardware. Actual NPU use is claimed only after the Runtime page and strict QNN report verify it.
