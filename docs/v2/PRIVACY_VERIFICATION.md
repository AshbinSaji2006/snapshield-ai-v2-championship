# SnapShield AI v2 — privacy verification

## Production analysis boundary — verified

- Desktop service binds to loopback.
- Core ML, OCR, QR, URL, brand, PII, graph, fusion, and incident operations use local libraries/artifacts.
- URL analysis performs no navigation or DNS/reputation request.
- No cloud AI client is part of the production analysis path.
- Tests block network calls during production analysis.
- Incident storage excludes raw source and stores sanitized derived metadata plus a source hash.
- Live Shield is off by default and saves only by explicit user choice.

## Developer Qualcomm workflow — separate and opt-in

`scripts/snapdragon/run_aihub_validation.py` is a developer-triggered model compilation/profiling workflow. It may upload a model artifact to Qualcomm AI Hub after the developer configures credentials and deliberately runs the script. It is not imported or called by normal SnapShield analysis and does not upload user content.

## Claim boundary

Approved: “Core analysis runs locally after installation; no cloud AI is required.”
Not approved: “The device or operating system can never transmit any data.”
