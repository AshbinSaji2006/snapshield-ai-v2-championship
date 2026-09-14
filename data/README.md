# Data directory

- `raw/` contains the checksum-pinned UCI archive and attribution.
- `processed/uci_sms/` contains reproducible deduplicated train/validation/test TSVs and a manifest.
- `samples/` contains inert, project-authored demonstration inputs using reserved/example destinations.
- `snapshield.db` is created locally at source runtime and ignored by Git; the packaged build uses `%LOCALAPPDATA%/SnapShieldAI`.

Raw user/production input must never be copied into this repository.
