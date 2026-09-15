# Windows ARM64 Build

Current development host: Windows 11 AMD64. No AMD64 artifact is labeled ARM64 and no native ARM64 package has been produced.

PyInstaller is not a cross-compiler. The legitimate build path is a Windows-on-ARM64 machine with ARM64 Python and native ARM64 wheels for every runtime dependency:

1. Clone/check out the frozen v2 release commit on Windows ARM64.
2. Install current ARM64 Python 3.12 and Node.js.
3. Create `.venv` and install `requirements.txt`; verify each binary wheel architecture, especially ONNX Runtime/QNN, OpenCV, tokenizers, scikit-learn and RapidOCR dependencies.
4. Build the frontend with `npm ci`, `npm run lint`, `npm run typecheck`, and `npm run build`.
5. Install the current Qualcomm QNN/ONNX Runtime plugin package according to its release documentation and compatible QAIRT version.
6. Run the complete backend suite and a strict QNN session with CPU fallback disabled.
7. Run `pyinstaller SnapShieldAI.spec --noconfirm --clean` natively.
8. Verify the PE machine field is ARM64 (`0xAA64`) using `dumpbin /headers` or an equivalent trusted tool.
9. Repeat smoke, OCR/QR, provider, red-team and checksum gates on that device.

Status: **Native ARM64 build pending an ARM64 Windows build environment.**
