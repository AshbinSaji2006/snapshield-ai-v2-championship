# Limitations

- UCI and Mendeley results measure named SMS datasets, not universal phishing, malware or fraud detection.
- The Mendeley set was published in 2022. It is cross-domain evidence, not a current-2026 threat feed.
- India-focused English/Hinglish/Romanized-Hindi checks are a curated functional suite, not multilingual accuracy. Deep Guard is an English compact encoder and is skipped for unsupported Devanagari input.
- Domain mismatch is a heuristic. Legitimate third-party services exist; the UI asks users to verify independently.
- No URLs are fetched, so SnapShield does not inspect live page content, redirects, reputation, certificates or domain age.
- OCR quality depends on resolution/layout. Current CPU OCR is materially slower than text analysis and can miss stylized content.
- QR decoding does not navigate. An undecoded QR is not evidence of safety.
- Live Shield supports Windows text clipboard only, is off by default, and is not an antivirus or keylogger.
- Current verified execution provider is CPU. Qualcomm AI Hub, QNN/NPU and native ARM64 validation remain pending.
- No power, energy, battery, thermal or Snapdragon latency benefit has been measured.
- The Threat Evidence Graph is deterministic correlation/provenance, not causal proof or graph ML.
- Local analysis reduces content exposure but cannot protect a compromised operating system or another process with local access.
