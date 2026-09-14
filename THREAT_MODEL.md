# Threat model

Assets are private user content, incident metadata, model integrity, local service integrity, and the user's security decision. Adversaries include remote phishers crafting evasive inputs, malicious image files, hostile websites probing localhost, and malware/local users on the PC.

| Threat | Control | Residual risk |
|---|---|---|
| Content exfiltration | No cloud client; loopback bind; local-origin/host controls | Compromised host can observe memory |
| URL-triggered attack/SSRF | Parse only; no DNS, HTTP, redirect expansion, or navigation | Reputation and destination context unavailable |
| Image parser abuse | Byte, pixel, MIME, format, and verification gates | Native decoder vulnerabilities remain possible |
| Traversal/static exposure | Demo allowlist and resolved containment; unknown API 404 | Future routes/assets require equivalent review |
| Browser-to-local abuse | Origin rejection, narrow CORS, JSON API, trusted hosts | Production shell still needs per-launch token |
| Stored secret exposure | No raw input; masked/sanitized evidence; local database | Common-input hashes can be guessed |
| SQL injection | Parameterized statements | Schema/library flaws remain possible |
| XSS | React text rendering and CSP; no raw HTML API | Dependency/browser flaws remain possible |
| Model evasion | ML plus independent URL/text/brand/PII/QR evidence | Novel, multilingual, and contextual attacks can evade |
| Score manipulation | Capped fusion, corroboration discount, regression cases | Heuristic weights are not formal probabilities |
| Provider spoofing | Verification JSON plus provider/session checks | Target graph assignment still requires QNN profiling |
| Resource exhaustion | Per-request text/image limits | No process-wide concurrency/rate budget |

The system is decision support, not antivirus or a guarantee of safety.
