# Championship execution log

Started 2026-09-15 (Asia/Kolkata). Only this v2 workspace is editable.

## Plan and gates

1. Preserve the complete v1 tree, verify SHA-256, import and tag Git baseline; run unchanged tests.
2. Verify primary Qualcomm/toolchain/model/data sources. Resolve AI Hub account availability early.
3. Acquire original licensed cross-domain evaluation data; quarantine duplicates against all UCI splits.
4. Compare compact pretrained neural candidates on validation only; preserve Fast Guard artifacts. Export/evaluate selected candidate and calibration. No test-based tuning.
5. Build explainable routing, bounded normalization, offline domain evidence, provenance graph, and safe optional clipboard monitoring.
6. Verify regressions, exfiltration behavior, adversarial robustness, fallback, frontend, and dependencies.
7. Attempt exact-artifact AI Hub compile/profile; retain pending status if authentication/hardware blocks execution. Prepare native ARM64 recipe.
8. Freeze only after quality gates, produce real screenshots and v2 submission assets, hash final artifacts, and reverify v1.

## Evidence already found

- Complete v1 inventory: 6,818 files / 600,784,888 bytes. Byte-preserving backup outside the v2 workspace. All 6,818 backup files verified.
- Git baseline tag: `v1.0-frozen-competition`; development branch: `v2-championship`.
- Windows AMD64, 15.72 GiB RAM, RTX 3050 Laptop 6 GiB. GPU available for development training; not a Snapdragon device.
- v1 training code refits selected model on train + validation. Frozen Fast Guard must not be calibrated against its in-sample validation predictions. Use out-of-fold train+validation predictions for calibration; use a train-only shadow baseline for selection comparisons.
- AI Hub client credentials absent at initial check. User configuration requested asynchronously; local work continues.
- Mendeley public API route resolved from original site's client: `/public-api/datasets/f45bkkt8pr/files?folder_id=root&version=1`. The original archive publishes its SHA-256, enabling verified acquisition without a mirror.

This is an active execution log, not a completion claim.
