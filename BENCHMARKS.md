# Benchmarks

These results were recorded on 2026-09-12 on `Windows-11-10.0.26200-SP0`, Intel AMD64, Python 3.12.6, ONNX Runtime 1.30.0, using `CPUExecutionProvider` and `text_classifier.onnx`. They are development-machine timings, not Snapdragon results and not power measurements.

## Component-separated results

`python scripts/benchmark.py` warms each operational component unless the row is explicitly cold. Incident persistence and browser rendering are excluded.

| Workload | Iterations | Mean ms | Median ms | P95 ms | Min ms | Max ms |
|---|---:|---:|---:|---:|---:|---:|
| Cold ONNX model + vectorizer load | 10 | 198.1020 | 122.3451 | 395.6139 | 112.2359 | 395.6139 |
| URL rule analysis | 500 | 0.0843 | 0.0789 | 0.1094 | 0.0611 | 0.5766 |
| TF-IDF preprocessing | 300 | 0.6653 | 0.6348 | 0.9020 | 0.4846 | 1.5462 |
| ONNX inference only | 500 | 0.0978 | 0.0798 | 0.2149 | 0.0602 | 0.5110 |
| PII detection/redaction | 500 | 0.1106 | 0.1075 | 0.1537 | 0.0837 | 0.4268 |
| QR decode | 100 | 35.6743 | 34.4180 | 46.7230 | 30.4307 | 53.3847 |
| Full text security pipeline | 200 | 5.3033 | 5.0894 | 8.0208 | 3.0989 | 9.9047 |
| OCR screenshot | 10 | 5382.9855 | 4648.2198 | 7948.9731 | 2255.7386 | 7948.9731 |
| OCR + full security pipeline | 10 | 1926.8773 | 1903.7909 | 2160.0915 | 1720.2950 | 2160.0915 |
| OCR + QR + full security pipeline | 10 | 1858.7367 | 1863.3500 | 1960.7212 | 1731.0035 | 1960.7212 |

The standalone OCR row had substantial local variability despite a warm-up; the later end-to-end rows demonstrate the stabilized run. These rows use different sample images, so they are not algebraically comparable. Full raw metadata is in `benchmarks/results/component_benchmark.json`.

## ONNX validation-run timing

The hardware-validation script completed 100 inference-only CPU iterations: mean 0.0352 ms, median 0.0288 ms, p95 0.0366 ms, min 0.0235 ms, max 0.6609 ms. It also recorded a 12,288-byte process-memory delta and exact reference/target probability agreement for its test input. This workload precomputes TF-IDF features and therefore must not be described as full text latency.

## Interpretation

- URL/rule and PII timings are deterministic engine microbenchmarks.
- `ONNX inference only` excludes TF-IDF preprocessing.
- `Full text` includes text rules, TF-IDF, ONNX, embedded URL analysis, brand checks, PII, fusion, explanation, and recommendations.
- Screenshot rows include real local RapidOCR; the multimodal row also performs OpenCV QR decode.
- UI/API transport and optional SQLite persistence are not included.
- No CPU-versus-NPU comparison is available because no QNN provider or Snapdragon device was present.

## Reproduction and target protocol

Run `python scripts/benchmark.py` for component timings and `python scripts/snapdragon/validate_snapdragon.py` for provider/hardware validation. On target Snapdragon hardware, install a compatible native ARM64 ONNX Runtime QNN/Windows ML provider, run with CPU fallback disabled, verify output agreement, then compare identical model/input/warm-up/iteration settings. Record exact SoC, OS, runtime, provider assignment, memory, and any power tool used.
