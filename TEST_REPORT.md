# Test report

## Final automated gate

Verified 2026-09-13 on Windows 11 build 26200, AMD64, Python 3.12.6:

| Check | Result |
|---|---|
| Backend pytest | **77 passed** in 12.18 s after final visual-build verification |
| Frontend lint | Passed, zero warnings (`oxlint 1.82.0`) |
| Strict TypeScript | Passed (`typescript 7.0.2`) |
| Vite production build | Passed (`vite 8.3.0`) |
| Production JS | 256.40 kB / 79.89 kB gzip |
| Production CSS | 20.69 kB / 5.49 kB gzip |
| npm production audit | 0 vulnerabilities |
| Python dependency consistency | `pip check`: no broken requirements |
| Python vulnerability audit | `pip-audit`: no known vulnerabilities |

The 77 tests cover URL parsing/defanging/obfuscation, text rules and model inference, risk calibration, brand mismatch, PII/Luhn/redaction, ONNX primary inference, scikit-learn fallback agreement, provider truthfulness, exact QNN artifact-hash gating, SQLite lifecycle/statistics/deletion/sanitized evidence, API errors, origin blocking, security headers, demo allowlisting/path handling, image MIME/format/pixel limits, real RapidOCR extraction, low-resolution OCR context, and real QR-to-URL analysis.

## Model and adversarial verification

- Three models compared on the validation split; untouched test metrics generated and saved.
- FP32 ONNX versus scikit-learn: 766/766 test records, 100% class agreement, max probability difference `9.24e-8`.
- QDQ versus FP32: 99.739% class agreement at 0.5 on 766 test records; quantization calibration used validation data only.
- Curated functional/adversarial suite: 18/18 expected risk bands. This is not reported as model accuracy.

## End-to-end checks

- Source FastAPI app: health/database ready, runtime metadata, text, URL, OCR image, QR image, PII redaction, incident create/get/delete, stats, and production SPA routes exercised.
- Multimodal asset: RapidOCR extracted text with high confidence, OpenCV decoded one QR, and the combined real pipeline returned critical risk.
- Packaged executable: launched headlessly on `127.0.0.1:8765`; `/api/health` returned `ok`, the named ONNX model loaded on CPU, and a phishing text returned score 100/critical.
- Windows artifact: 1,363 files, 390,359,552 bytes (372.28 MiB), `NotSigned`.

## Commands

```powershell
python -m pytest
python scripts/evaluate_security_cases.py
python scripts/benchmark.py
python scripts/snapdragon/validate_snapdragon.py
cd frontend
npm run lint
npm run typecheck
npm run build
npm audit --omit=dev
```

Hardware validation is separate: the script passed CPU correctness but correctly produced `verified: false` because QNN/Snapdragon was not available.
