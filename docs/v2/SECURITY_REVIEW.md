# SnapShield AI v2 — security and privacy review

## Result

PASS for the documented local application threat boundary, with limitations below. This is an application review, not a formal penetration test or third-party certification.

## Reviewed controls

- FastAPI binds the desktop build to `127.0.0.1`, not a public interface.
- Submitted URLs are parsed without navigation, DNS resolution, redirect following, or payload execution.
- Invalid ports and invalid IDNA are rejected safely.
- Original and normalized text representations are separated so defanging/confusables can be inspected without silently rewriting the source.
- Image routes enforce type/size controls before defensive decoding.
- QR payloads are decoded and displayed, never opened automatically.
- Risk fusion caps evidence families and elevates combinations, reducing repeated-signal double counting.
- Raw submitted content is excluded from incident storage; graph fields use masked/sanitized values.
- Live Shield is off by default, requires consent, deduplicates and rate-limits checks, and saves only by explicit action.
- React output escaping and hostile-markup regression cases reduce stored/reflected script injection risk.
- Deployed neural execution is hash-gated; QNN validation additionally requires exact compiled-artifact identity and strict provider evidence.

## Tested abuse cases

The 100-test suite includes zero-width/defanged input, unsupported script handling, invalid IDNA and ports, brand mismatch, request oversize, hostile markup, network-call blocking, PII-safe graph/export, Live Shield consent/deduplication/rate limiting, provider/hash validation, and a real Deep Guard inference.

The 20-case functional suite covers safe and suspicious forms of Punycode, homoglyphs, spaced URLs, shorteners, official/mismatched brands, credentials/payments, Hinglish KYC, Romanized electricity, UPI refund, digital arrest, job fee, and customs lures. It is a curated regression suite, not a statistical security rate.

## Dependency review

At the recorded final audit, `pip check` was clean, the Python advisory audit reported no known vulnerabilities, and `npm audit --omit=dev` reported zero vulnerabilities. These results expire as advisories and packages change.

## Residual risks

- A compromised endpoint can still read screen, clipboard, process memory, or local files.
- Heuristics and ML can produce false positives and false negatives; low risk is never a guarantee.
- URL analysis lacks live reputation, DNS, certificate, redirect, and landing-page context by design.
- OCR is slower and can fail on low-resolution, stylized, multilingual, or complex layouts.
- The finite brand/domain map cannot cover every brand or legitimate delegated domain.
- The build is unsigned AMD64; SmartScreen/reputation and native ARM64 remain external work.
- QNN assignment, NPU latency, energy use, and battery impact remain unverified.

## Red-team conclusion

No discovered issue blocks the competition demo within its stated boundary. The strongest remaining technical risks are detection coverage and unavailable target-hardware proof, both disclosed in the product and submission materials.
