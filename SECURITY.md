# Security policy

## Implemented controls

SnapShield treats all content as hostile data. It does not render submitted HTML, fetch or navigate to submitted URLs, perform DNS resolution, execute payloads, or call cloud AI.

- FastAPI/Pydantic request validation and a 50,000-character text cap.
- Loopback-only documented/packaged binding, trusted-host allowlist, restricted local origins/CORS, CSP, `nosniff`, and no-referrer headers.
- Image MIME and decoded-format allowlists, 10 MiB byte cap, 25-megapixel decoded cap, and Pillow verification before OCR/QR libraries process pixels.
- Demo filename allowlist, resolved static-path containment, and 404 handling for unknown/normalized API paths.
- Parameterized SQLite statements.
- React escaped rendering; no `dangerouslySetInnerHTML`.
- Raw messages/images/full URLs/secrets are excluded from logs and incident storage. Only sanitized evidence and hashes persist.
- ONNX initialization falls back locally; no remote model loading occurs.

Automated tests cover malformed files, wrong MIME/format, pixel limits, traversal/allowlisting, hostile origins, headers, URL schemes, redaction, and database lifecycle.

## Residual risks

- There is no global rate limiter; loopback malware or a hostile local user could cause resource exhaustion.
- A compromised host can observe browser/process memory and local database files.
- Native OpenCV/Pillow/ONNX/OCR parsers expand the attack surface and require updates.
- Hashes of predictable source messages may be guessable.
- Structural URL analysis has no live reputation or redirect context.
- OCR/model/rule errors and novel evasion remain possible; low risk is never a guarantee.
- The Windows artifact is unsigned and lacks a secure updater/per-launch API token.

## Dependency review

On 2026-09-12, an initial `pip-audit` found advisories in the old FastAPI/Starlette, python-multipart, Pillow, and pytest stack. Those packages and the Starlette test client dependency were upgraded; the final `pip-audit -r requirements.txt` reported no known vulnerabilities and `pip check` reported no broken requirements. Full `npm audit --offline` reported zero vulnerabilities. This is a point-in-time check, not a guarantee that dependencies are vulnerability-free.

Use SnapShield as decision support. Confirm credential or financial requests through a separately obtained trusted channel. For security reports, privately contact the repository owner without including real secrets or victim data.
