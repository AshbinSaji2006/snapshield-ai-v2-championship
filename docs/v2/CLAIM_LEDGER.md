# Claim Ledger

| Claim | Status | Evidence / artifact | Allowed wording | Forbidden wording |
|---|---|---|---|---|
| v1 preserved | VERIFIED | external v1 inventory, SHA-256 manifest and verification JSON | “v1 was copied and hash-verified before v2 work” | “v1 was untouched” without manifest evidence |
| UCI Fast Guard result | VERIFIED | `ml/artifacts/model_metadata.json`; named 766-message test | “98.17% accuracy on the deduplicated UCI SMS Spam Collection test” | “98.17% phishing accuracy” |
| Deep Guard UCI | VERIFIED | `reports/v2/model_evaluation.json` | “94.44% recall on the 766-message UCI test” | universal detection claims |
| Deep Guard cross-domain | VERIFIED | same report; 521-record hash | “98.04% recall on the independently deduplicated 2022 Mendeley holdout” | “2026/current-threat accuracy” |
| Adaptive v2.2 | VERIFIED WITH DISCLOSURE | `adaptive_routing_evaluation_v2.2.json` | “matched Deep recall while escalating 33.68%/51.25%; v2.2 followed a disclosed v2.1 cross-domain failure” | “untouched adaptive cross-domain benchmark” |
| ONNX equivalence | VERIFIED | experiment JSON and quantization report | “100% class agreement across 766 validation messages” | bit-exact output |
| QDQ equivalence | VERIFIED | `reports/v2/model_evaluation.json` | “100% FP32 class agreement on the two reported evaluation sets” | “NPU optimized” or faster without measurement |
| Functional robustness | VERIFIED | `reports/v2/functional_evaluation.json` | “20/20 curated functional checks” | “multilingual/Hindi accuracy” |
| Offline core | VERIFIED | network-disabled test; no-fetch URL design | “normal production analysis needs no cloud AI or URL fetch” | “the app can never access a network” |
| Privacy | VERIFIED WITH SCOPE | API, DB allowlist, network test, Live Shield tests | “source content is not persisted by normal analysis” | “mathematically guaranteed privacy” |
| Threat Evidence Graph | VERIFIED | API output/tests | “structured local evidence-correlation graph” | “graph neural network” or proof of maliciousness |
| Live Shield | VERIFIED | implementation/tests | “opt-in local Windows text-clipboard monitoring” | keylogging, antivirus or silent monitoring claims |
| Local provider | VERIFIED | runtime API/current machine | “CPUExecutionProvider is active” | GPU/NPU active |
| Qualcomm AI Hub | PENDING | missing local config; handoff | “validation automation implemented; authentication pending” | compile/profile completed |
| Snapdragon NPU/QNN | IMPLEMENTED BUT UNVERIFIED | scripts/runtime gates | “Snapdragon-ready ONNX/QNN path; hardware validation pending” | “NPU verified/accelerated” |
| ARM64 executable | PENDING | `ARM64_BUILD.md` | “reproducible native ARM64 build instructions” | calling AMD64 build ARM64 |
| Latency | VERIFIED ON CURRENT PC ONLY | `reports/v2/unified_benchmarks.json` | quote operation, provider, hardware and repetitions | Snapdragon latency or power inference |
| Power efficiency | NOT MEASURED | none | “potential benefit to validate” | wattage, battery or efficiency improvement |
