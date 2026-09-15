# SnapShield AI v2 — public repository audit

## Publishable source state

- No credentials, API keys, private keys, or configured Qualcomm AI Hub client file are intentionally included.
- `.env`, logs, runtime databases, caches, virtual environments, `node_modules`, frontend build output, PyInstaller output, and releases are Git-ignored.
- Raw Mendeley CSV/ZIP and the message-bearing processed external holdout are Git-ignored; versioned provenance and a non-content manifest retain reproducibility metadata.
- Dataset attribution and CC BY 4.0 terms are recorded in `DATASETS.md` and `docs/v2/DATA_PROTOCOL.md`.
- The deployable Fast/Deep ONNX artifacts and manifests are part of the intended source release; large-file hosting policy should be confirmed before publication.
- The Windows one-folder binary should be attached as a release artifact, not committed to normal source history.

## Publication status

`PUBLIC_REPOSITORY_URL_PENDING`

No repository was created or published automatically. Before publication, the owner must review Git’s staged file list, confirm identity/license metadata, choose Git LFS or release assets if the host rejects model size, and create the public remote.

## Human pre-push commands

```powershell
git status --short
git diff --cached --stat
git grep -n -I -E "(api[_-]?key|client[_-]?secret|BEGIN .*PRIVATE KEY)"
git ls-files | ForEach-Object { Get-Item -LiteralPath $_ } | Sort-Object Length -Descending | Select-Object -First 20 FullName,Length
```
