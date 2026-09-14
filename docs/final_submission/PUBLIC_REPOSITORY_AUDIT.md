# Public Repository Readiness Audit

Audit date: **2026-09-13**

Status: **PASS for the source tree; publication remains pending because this folder is not a Git worktree and GitHub CLI is unavailable.** Apply the existing ignore policy, review the exact staged list, and assign the real public URL before publishing.

## Verified

- No real private key, AWS key, GitHub token, OpenAI-style secret, API credential, or bearer token was found by the final filename/content scan.
- Apparent secret-pattern matches are intentional detection regexes and synthetic test literals in `backend/app/pii_analyzer.py` and `backend/tests/test_pii_analyzer.py`.
- `.env.example` contains only loopback host/port defaults and explicitly requires no cloud API key.
- Root `LICENSE` and `THIRD_PARTY_NOTICES.md` are present.
- UCI SMS Spam Collection attribution is present in `README.md`, `DATASETS.md`, `MODEL_CARD.md`, `data/raw/ATTRIBUTION.md`, and `THIRD_PARTY_NOTICES.md` with DOI `10.24432/C5CC84` and CC BY 4.0 licensing.
- The pinned raw archive is 203,415 bytes and supports reproducibility; its source, checksum, and license are documented.
- Source files contain no hard-coded personal workspace path. Local-path matches were confined to ignored PyInstaller build reports.
- All 16 Markdown links/images in `README.md` resolve, and the README contains no `D:\` filesystem path.
- No browser profile, real screen recording, private URL, or unrelated large binary was found in the publishable source set.

## Must remain excluded from a public source commit

- `data/snapshield.db` — local incident database; ignored by `data/*.db` and intentionally preserved on this machine.
- `build/`, `release/`, `frontend/dist/`, `frontend/node_modules/`, `.venv/`, `__pycache__/`, `.pytest_cache/`, `.pytest-temp/`, logs, and local `.env` files.
- The 372.28 MiB AMD64 executable bundle should be distributed as a release asset or through an appropriate large-file channel, not committed into ordinary source history.

## Large-file decision

- Keep the 203,415-byte pinned UCI source archive and prepared splits: they are small, licensed, attributed, checksummed reproducibility assets.
- Keep the compact trained vectorizer/ONNX artifacts required to run the project.
- Keep the real PNG screenshots and architecture/privacy graphics under `docs/final_submission/assets/`; they are central review evidence and each is below 400 KB.
- Do not commit `release/SnapShieldAI`, the competition ZIP, PPTX, PDF, PyInstaller build cache, OCR/runtime dependency bundles, or virtual environments. Publish finalized binaries separately only if the chosen release channel accepts them.

## Boundary

Git 2.46.2 is installed, but the directory is not currently attached to Git metadata and GitHub CLI is unavailable. Commit history, staged files, branch protection, remote settings, and authenticated publication therefore could not be audited. Before publication, initialize or connect the repository, review the exact staged file list, and replace `PUBLIC_REPOSITORY_URL_PENDING` only with the real URL.
