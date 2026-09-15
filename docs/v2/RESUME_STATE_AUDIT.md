# SnapShield AI v2 — Resume State Audit

Audit time: 2026-09-15 (Asia/Kolkata)
Workspace: `snapshield-ai-v2-championship`
Purpose: reconstruct the interrupted session from filesystem evidence before further engineering.

## Git state

- Branch: `v2-championship`
- Frozen baseline commit: `cc00565cfcdad55046873e9f8a4719a032591244`
- Baseline tag: `v1.0-frozen-competition`
- Latest commit: the frozen import commit above; all championship work is intentionally still in the working tree.
- Modified tracked files at resume: `.gitignore`, eight backend application modules, `desktop_launcher.py`, and `frontend/src/types.ts`.
- Untracked work at resume: seven backend v2 modules, offline PSL resources, Mendeley manifests/processed holdout, three v2 research notes, two championship frontend files, three experiment records/prediction arrays, the v2 training requirements, and three acquisition/training scripts.
- The frozen v1 source tree was not modified during this audit. Its previously generated inventory and full backup hash verification remain the preservation evidence.

## Neural experiment recovery

All three planned candidates completed after the interrupted session. Each has a SafeTensors checkpoint, tokenizer/config, ONNX export, validation predictions, and an experiment JSON. The final UCI test was not read by the tournament (`test_read: false`).

| Candidate | Best epoch | Selection recall | Macro F1 | FPR | PR-AUC | Calibrated Brier | ONNX bytes | CPU median / P95 | ONNX agreement | ONNX SHA-256 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---|
| BERT Tiny L2/H128 | 4 | 91.11% | 97.38% | 0.00% | 97.72% | 0.01025 | 17,515,277 | 3.25 / 5.16 ms | 100% of 766 | `71a4a43e36f5ef23845e28953b0a05785f6bf71c1785680f531e70efefe33f3f` |
| MiniLM L6 | 1 | 93.33% | 96.22% | 0.89% | 97.02% | 0.01104 | 90,341,665 | 48.47 / 62.93 ms | 100% of 766 | `38ea26aeb10f9618f8f347d6d3840f515c0e8c64d818f96ee7fc56e15b280ad3` |
| DistilBERT | 1 | 93.33% | 96.82% | 0.59% | 97.14% | 0.01364 | 265,522,903 | 153.22 / 650.34 ms | 100% of 766 | `74889e8a7822fd5b05d6d1293cedc6b8648f31e228a0b44230dfadc64c25ece1` |

Checkpoint hashes:

- BERT Tiny: `e56c637d04f55d01e4cc2af54990711ee3c0e2ff66003f69048b909259352113` (17,548,868 bytes)
- MiniLM L6: `846e11622340d99b429d9baF58f3a0c8bdd1529f8f34fa3bfe65dcc83ed2d6c0` (90,866,684 bytes)
- DistilBERT: `aabf3ee47ca93098c23d4419b6f782b6d4b49df208a6177bef2cf1211e49631a` (265,466,612 bytes)

The tournament is complete; no stale training process needs resumption. Candidate selection remains validation-only and will be frozen before the one-time final-test evaluation.

## Dataset verification

- UCI source: SMS Spam Collection, CC BY 4.0, source archive SHA-256 `1587ea43e58e82b14ff1f5425c88e17f8496bfcdb67a583dbff9eefaf9963ce3`.
- Deduplicated UCI corpus: 5,105 records; train 3,573, validation 766, untouched test 766.
- UCI split hashes: train `f690277f868451e7bee33bd50d5b212914a864ae5330efeade8669c0e8136b70`; validation `b0d8fb5aa0c29e8fd4930417901c3f4c0c9f9714da7de3db8a659455b4d688c8`; test `26bd13efd5a772a05cb63e1a859dc74260d81e585442ac1ca81f0ff430ceb343`.
- Mendeley SMS Phishing source archive SHA-256: `9bbf3188fdad81495d8e82825648b9b63b53fc86841a3d26c02629990b233cc3`, matching the publisher value.
- Extracted source CSV SHA-256: `649844f1c62a6b27e145eaf17a65f7010c56c390e11a794ea8329993a05ba71e`.
- Provenance/license: Mendeley dataset DOI `10.17632/f45bkkt8pr.1`, CC BY 4.0, published in 2022. It is not described as a current-2026 benchmark.
- Exclusions: 5,123 normalized overlaps with UCI, 231 near-overlaps with UCI, 69 internal normalized duplicates, 26 internal near-duplicates, and one conflicting-label record.
- Independent retained holdout: 521 records: 317 ham, 87 spam, 117 smishing. Holdout SHA-256 `0b984c45b333e916fb1b6f61ac60b044f9d8dbb21270602a476e738422c7063f`.
- Role is fixed as cross-domain evaluation only; it was not used for learning, selection, calibration, or routing design.

## Application implementation recovered

- `normalization.py`: bounded original-versus-normalized security representation and obfuscation evidence.
- `adaptive.py`: explicit Fast-only / escalation policy and route reasons.
- `deep_guard.py`: optional hash-gated ONNX runtime with safe Fast Guard fallback.
- `domain_intelligence.py`: offline Public Suffix List parsing, Unicode host facts, and edit distance.
- `evidence_graph.py`: structured provenance-bearing evidence nodes/relationships and sanitized export.
- `india_security.py`: curated India-focused deterministic patterns; no multilingual-accuracy claim.
- `live_shield.py`: opt-in, volatile, deduplicated and rate-limited Windows clipboard analysis.
- Existing orchestrator, URL, brand, runtime and API modules were extended to call these components.
- `Championship.tsx` and `championship.css` contain the adaptive-routing, evidence-graph and Live Shield surfaces but were not yet integrated into the main app at interruption.

## Tests and quality state

- No v2-specific test files existed at resume.
- The full inherited backend suite passes: **77 passed**.
- Frontend lint/typecheck/build initially identify one incomplete JSX closure in the unintegrated `Championship.tsx`; this is a recovered partial edit, not a baseline regression.

## Qualcomm/runtime state

- Python client: `qai-hub 0.55.0` installed.
- Local inference stack: `onnxruntime 1.30.0`, `onnx 1.22.0`, `tokenizers 0.23.1`, `transformers 5.17.0`.
- AI Hub configuration file is absent at `%USERPROFILE%/.qai_hub/client.ini`; an authentication test fails before any job submission.
- `AI_HUB_AUTH = PENDING`.
- No Qualcomm job ID, compiled artifact, Snapdragon measurement, QNN/NPU execution, or NPU verification exists. Current local runtime remains CPU.

## Resume decision

Preserve all completed candidates and select the edge-security Pareto winner from the fixed validation evidence. Then perform the single final UCI test read, cross-domain evaluation, router evaluation, ONNX/quantization gates, integration, tests and security work. Qualcomm validation proceeds automatically if local credentials become available; otherwise it remains truthfully pending with a reproducible handoff.
