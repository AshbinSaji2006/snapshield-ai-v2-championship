# Threat Evidence Graph

The Threat Evidence Graph is structured correlation output, not graph machine learning and not a decorative diagram. `backend/app/evidence_graph.py` emits stable typed nodes for input sources, OCR text, QR payloads, URLs, domains, claimed/expected brands, model/rule findings, routing and the final decision. Typed edges record extraction, hostname, claim, expected-domain, conflict, routing and contribution relationships.

Every graph carries a schema version and an explicit warning that relationships represent extraction/rule correlation rather than proof of malicious intent. Node labels/evidence are passed through PII redaction; URL nodes use ordinal IDs so hashes do not leak secret paths. The default UI presents a bounded set of high-value nodes and allows keyboard/click exploration of provenance and contribution details.

Machine-readable graph output appears at `details.evidence_graph` for text, URL and image analyses. Sanitized incident export uses a separate allowlist and excludes source content, URLs, input hashes and extracted PII.
