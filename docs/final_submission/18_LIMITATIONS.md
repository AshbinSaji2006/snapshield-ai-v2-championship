# Limitations and Honest Boundaries

## Current limitations

1. **No verified Snapdragon NPU run.** The current audited machine is AMD64 and selects ONNX Runtime CPU. QNN and device performance are pending compatible hardware.
2. **SMS-focused training data.** The model was trained and tested on the UCI SMS Spam Collection, not a comprehensive modern phishing, email, QR, multilingual, or enterprise dataset.
3. **Recall is not complete.** The test split contains 12 false negatives out of 90 spam examples, producing 86.6667% recall.
4. **Classifier metrics are not end-to-end metrics.** The 98.1723% accuracy result applies to the compact text classifier and fixed test split, not the complete multimodal product.
5. **OCR is input-quality dependent.** Blur, unusual fonts, low contrast, layout complexity, handwriting, and adversarial images can reduce text extraction quality.
6. **QR decoding is not semantic truth.** A decoded payload can be inspected structurally, but an undecodable or visually manipulated code can escape that path.
7. **No reputation or live destination lookup.** URLs are intentionally never opened. This improves safety and privacy but means SnapShield does not use live domain age, redirect chains, certificates, takedown feeds, or page content.
8. **Rule coverage is finite.** Attackers can rephrase persuasion cues, encode content, use new TLDs, or exploit languages and brands outside the current rules.
9. **Risk scores are not calibrated probabilities.** They are bounded evidence-weighted operational scores.
10. **English-centric behavior.** The dataset and current lexical patterns primarily represent English-language content.
11. **Local endpoint trust remains necessary.** If the host is already compromised, malware with sufficient privileges could inspect process memory, modify artifacts, or interfere with the local service.
12. **Persistent metadata still exists.** Although source content is excluded, incident hashes, timestamps, classifications, scores, timings, and sanitized indicator names remain until deleted.
13. **Packaged build is unsigned.** The verified AMD64 executable reports `NotSigned`, which may trigger Windows trust warnings and is not appropriate for broad production deployment.
14. **CPU benchmark scope is narrow.** Results come from one development machine and exclude browser rendering and persistence.
15. **No automated remediation.** SnapShield advises; it does not block URLs, quarantine content, change browser settings, or act on user accounts.

## Security posture statement

SnapShield is a decision-support prototype, not a replacement for endpoint protection, secure email gateways, browser isolation, identity controls, user training, or professional incident response. A low score is not proof of safety, and a high score is not proof of malicious intent.

## Responsible disclosure during judging

Lead with the working product and verified results, then state boundaries directly when relevant. Do not hide the SMS dataset behind the word “phishing,” turn a functional suite into an accuracy metric, or describe the implemented QNN path as completed NPU validation.

## Known risk mitigations already present

- Independent deterministic evidence reduces reliance on one model output.
- URLs are parsed without navigation.
- Source content is excluded from incident persistence.
- Provider identity is exposed rather than inferred.
- Fixed artifacts, hashes, and reports support reproducibility.
- CPU fallback preserves function when acceleration is absent.

These mitigations reduce risk; they do not eliminate the limitations above.
