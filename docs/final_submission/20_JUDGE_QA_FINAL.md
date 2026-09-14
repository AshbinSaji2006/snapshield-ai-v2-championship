# Final Judge Q&A

Use the short answer first. Give the deep answer only if the judge wants detail. Numbers and claim boundaries match [01_PROJECT_FACTS.md](01_PROJECT_FACTS.md).

## Product and problem

### 1. What is SnapShield AI?

**Short answer:** A local-first defense console that analyzes suspicious messages, URLs, screenshots, QR codes, and sensitive-data exposure.

**Deep answer:** It combines a compact ONNX text classifier with independent URL, social-engineering, OCR, QR, PII, and brand/domain checks. An evidence-fusion layer produces a risk score, explanation, and recommended action while excluding raw source content from persistent history.

### 2. What problem are you solving?

**Short answer:** People must judge fragmented scam evidence without either technical expertise or surrendering sensitive content to a cloud service.

**Deep answer:** Modern lures mix persuasive text, suspicious URLs, screenshots, and QR codes. SnapShield correlates those forms locally and turns technical indicators into a clear, actionable explanation.

### 3. Who is the primary user?

**Short answer:** Individuals and small teams who need a private second opinion on suspicious content.

**Deep answer:** The prototype is particularly useful where evidence may contain credentials, personal data, internal messages, or regulated information. An enterprise path would require deployment hardening, policy controls, broader evaluation, and security review.

### 4. What does “multimodal” mean here?

**Short answer:** The pipeline accepts text, URL, and image inputs and can extract both visible text and QR payloads from images.

**Deep answer:** Local OCR turns screenshot text into analyzable content, while OpenCV decodes QR data. Those outputs enter the same URL, language, privacy, and fusion stages rather than becoming separate disconnected verdicts.

### 5. Is this an antivirus replacement?

**Short answer:** No; it is decision support for suspicious content.

**Deep answer:** It does not scan binaries, monitor processes, quarantine files, or replace endpoint detection, secure email gateways, browser isolation, identity controls, or incident response. Its job is to explain content-level risk locally.

### 6. Does it automatically block threats?

**Short answer:** No; it recommends action but does not take account or system actions.

**Deep answer:** Automatic remediation would need stronger end-to-end validation, authorization design, rollback, and enterprise policy. The current product keeps the human in control.

### 7. Why is the product better than manually checking a message?

**Short answer:** It correlates several technical signals consistently and explains them in ordinary language.

**Deep answer:** A user may notice urgency but miss a numeric host, nonstandard port, QR destination, or brand/domain mismatch. SnapShield surfaces those independent clues together without visiting the destination.

### 8. What is the key innovation?

**Short answer:** Local multimodal evidence fusion with explicit privacy and hardware-verification boundaries.

**Deep answer:** The novelty is the system contract: compact ML plus deterministic forensic engines, traceable contributions, raw-source minimization, and provider claims based on measured runtime evidence rather than platform assumptions.

## Security behavior

### 9. Does SnapShield open suspicious links?

**Short answer:** No; it parses their structure but never navigates to them.

**Deep answer:** The URL engine examines scheme, host form, port, path, obfuscation, and related patterns. Avoiding navigation prevents the analysis itself from contacting a malicious destination.

### 10. Can it detect zero-day phishing sites?

**Short answer:** It can flag structural and persuasion indicators without a known-bad list, but it cannot guarantee zero-day detection.

**Deep answer:** Local heuristics can expose suspicious construction even when reputation data is absent. A polished benign page or novel phrasing may still evade detection, which is why a low score is not proof of safety.

### 11. How do you prevent false reassurance?

**Short answer:** The UI presents evidence and actions, not a guarantee that content is safe.

**Deep answer:** Results are bounded risk assessments, and limitations explicitly state that both false positives and false negatives exist. The product should support—not replace—user judgment and layered security controls.

### 12. How do you analyze defanged URLs such as `hxxp` or `[.]`?

**Short answer:** The normalization and detection path recognizes common defensive obfuscations without opening the destination.

**Deep answer:** Defanged indicators are treated as text evidence and reconstructed only for safe structural parsing where appropriate. The bundled obfuscated demo exercises that behavior with a reserved `.example` domain.

### 13. Can attackers evade the deterministic rules?

**Short answer:** Yes; rule coverage is finite, which is why rules are only one layer.

**Deep answer:** Attackers can rephrase, encode, fragment, or visually manipulate content. SnapShield combines rules with a learned text component and multimodal extraction, but broader corpora and ongoing error analysis remain necessary.

### 14. Why show indicator contributions?

**Short answer:** They let users see what changed the decision.

**Deep answer:** Contributions make the fusion process inspectable and help distinguish a single weak clue from several reinforcing signals. They are evidence weights, not causal or probabilistic guarantees.

### 15. Could the application itself contact the attacker?

**Short answer:** Its intended analysis path does not navigate to or fetch submitted URLs.

**Deep answer:** URL inspection is structural and local, and there is no cloud AI call. Production hardening should still include network-policy verification and continuous tests around every future integration.

### 16. Why not add live reputation lookup?

**Short answer:** The current design prioritizes offline operation, privacy, and no-contact analysis.

**Deep answer:** Reputation could improve coverage but would disclose indicators to a third party and create network dependency. It could be an explicit opt-in integration later, with a separate consent and retention boundary.

## Dataset and provenance

### 17. Where did the dataset come from?

**Short answer:** The UCI Machine Learning Repository’s SMS Spam Collection.

**Deep answer:** The recorded source is DOI `10.24432/C5CC84`, licensed CC BY 4.0 and accessed on 2026-09-12. The repository records the downloaded archive’s SHA-256 for provenance.

### 18. Was the dataset actually downloaded?

**Short answer:** Yes; the source archive was downloaded and its hash and preparation manifest are recorded.

**Deep answer:** The source began with 5,574 rows. The audited workflow retained 5,105 after deterministic duplicate handling, then created versioned train, validation, and test splits.

### 19. Why use an old SMS dataset?

**Short answer:** It is a licensed, reproducible baseline for the compact text component—not a complete modern phishing benchmark.

**Deep answer:** Its stable provenance supports an auditable competition build. Its age and narrow SMS domain are material limitations, so the roadmap adds current, multilingual, multimodal, and hard-negative datasets.

### 20. How did you handle duplicates?

**Short answer:** Duplicates were removed before splitting to reduce leakage.

**Deep answer:** Preparation removed 415 exact duplicates and 54 normalized near-duplicates, leaving 5,105 rows. No conflicting labels were found among normalized duplicates.

### 21. What are the split sizes?

**Short answer:** 3,573 train, 766 validation, and 766 test examples.

**Deep answer:** The 70/15/15 split was stratified with seed 42. Train contains 3,156 ham and 417 spam; validation and test each contain 676 ham and 90 spam.

### 22. Did you tune on the test set?

**Short answer:** No; candidate selection used validation data, and the test set was reserved for final evaluation.

**Deep answer:** Three predeclared candidates were compared through the documented selection process. QDQ calibration also used 300 validation examples and no test examples.

### 23. Is the dataset license compatible with this project?

**Short answer:** The source is recorded as CC BY 4.0, with attribution and provenance preserved.

**Deep answer:** The documentation names UCI, includes the DOI, license, access date, and source hash. A production data program would apply the same provenance discipline to every added corpus.

### 24. Does the corpus include screenshots and QR codes?

**Short answer:** No; the headline classifier dataset contains SMS text only.

**Deep answer:** OCR, QR, URL, PII, and fusion behaviors are tested separately. Product-level multimodal evaluation is a roadmap item and is not disguised as part of the SMS accuracy result.

## Model design

### 25. What model do you use?

**Short answer:** Word unigram/bigram TF-IDF feeding logistic regression, exported to ONNX.

**Deep answer:** The selected model is `snapshield_tfidf_logreg_word12_v1`, with 10,264 features, `C=7.0`, and class weights 1.0 for ham and 2.0 for spam. The deployable graph is a linear layer plus sigmoid.

### 26. Why such a simple model?

**Short answer:** It is small, fast, reproducible, deployable, and appropriate as one layer in an explainable local system.

**Deep answer:** Concrete URL, QR, PII, and persuasion evidence is handled by specialized modules, so the classifier need not solve every security task. Its simplicity also makes equivalence validation and constrained-device deployment practical.

### 27. Why not use an LLM or ChatGPT?

**Short answer:** A large remote model would weaken the privacy, offline, size, and reproducibility goals.

**Deep answer:** LLMs can improve semantic coverage, but they add memory, latency, nondeterminism, prompt-injection surface, and often cloud data transfer. A future compact local model must demonstrate measurable benefit under the same resource and evaluation budget before replacing this component.

### 28. Is logistic regression really AI?

**Short answer:** Yes; it is supervised machine learning, though the product’s value comes from the complete system rather than the label “AI.”

**Deep answer:** It learns weights from labeled examples and generalizes to unseen test samples. SnapShield deliberately avoids equating sophistication with model size.

### 29. Where is the TF-IDF transformation executed?

**Short answer:** Locally in the application pipeline before ONNX inference.

**Deep answer:** The featurizer maps normalized text into the fixed 10,264-feature contract. The ONNX graph consumes that numeric vector and performs `MatMul`, `Add`, and `Sigmoid`.

### 30. Why is the ONNX model only 41 KB?

**Short answer:** It contains a learned linear layer, while vocabulary and feature mapping are separate application artifacts.

**Deep answer:** Small size is expected for 10,264 linear weights plus bias and graph metadata. It is not evidence that the full product or featurization is only 41 KB.

### 31. Is the score a probability?

**Short answer:** The classifier emits a sigmoid score, but the displayed fused risk score is not presented as a calibrated probability.

**Deep answer:** Multiple evidence sources and policy weights affect the final 0–100 value. It is designed for consistent prioritization and explanation, not a statement such as “97% chance this is malicious.”

### 32. How do rules and ML interact?

**Short answer:** They generate independent evidence that a transparent fusion layer combines.

**Deep answer:** The model captures learned message patterns; deterministic engines capture auditable properties such as numeric hosts, urgent credential requests, PII, and brand mismatch. No single weak signal automatically becomes a universal verdict.

## Metrics and evaluation

### 33. What is your headline accuracy?

**Short answer:** 98.1723% on the fixed 766-message retained UCI SMS test split.

**Deep answer:** That is 752 correct classifications out of 766. It is a dataset-specific result for the text classifier, not a real-world phishing success rate for the entire application.

### 34. What are precision, recall, and F1?

**Short answer:** 97.5% precision, 86.6667% recall, and 91.7647% F1 for the spam class.

**Deep answer:** The model produced 78 true positives, 2 false positives, and 12 false negatives. Those counts make the recall limitation visible despite high overall accuracy.

### 35. Isn’t 98% misleading on an imbalanced dataset?

**Short answer:** It would be misleading alone, which is why we disclose the class counts, confusion matrix, precision, recall, F1, FPR, and PR AUC.

**Deep answer:** The test set contains 676 ham and 90 spam examples. Accuracy is one view; the 13.3333% spam false-negative rate is the important counterbalance.

### 36. What is the confusion matrix?

**Short answer:** `[[674, 2], [12, 78]]` for actual ham/spam rows and predicted ham/spam columns.

**Deep answer:** It means two legitimate messages were flagged as spam and twelve spam messages were missed. That corresponds to a 0.2959% false-positive rate and 86.6667% recall.

### 37. What are ROC AUC and PR AUC?

**Short answer:** ROC AUC is 0.992834 and PR AUC is 0.972218.

**Deep answer:** They summarize ranking across thresholds; PR AUC is particularly useful under class imbalance. They still describe this fixed corpus and do not remove the need for domain-specific evaluation.

### 38. How reproducible are the results?

**Short answer:** Data hashes, deterministic preparation, fixed seed and splits, selected parameters, reports, and model hashes are versioned.

**Deep answer:** Another reviewer can trace source acquisition through cleaned splits, selection, test evaluation, ONNX export, and package identity. Reproducibility does not imply broader external validity, which is documented separately.

### 39. What does 18/18 adversarial mean?

**Short answer:** Eighteen curated functional cases met their expected invariants; it is not an accuracy benchmark.

**Deep answer:** The suite checks behaviors such as obfuscation handling, redaction, and safe fusion. Its small hand-selected sample cannot support a statistical detection-rate claim.

### 40. Did you calculate confidence intervals?

**Short answer:** Not in the current canonical report.

**Deep answer:** The exact counts are provided so intervals can be computed transparently, but adding a post-hoc interval without pinning its method would create another inconsistent artifact. Formal interval and subgroup reporting belongs in the expanded evaluation phase.

## ONNX and deployment

### 41. Why ONNX?

**Short answer:** It provides a portable, inspectable deployment format supported by ONNX Runtime providers including CPU and QNN paths.

**Deep answer:** The format decouples training from deployment, makes input/output contracts explicit, and supports native-to-runtime equivalence checks. It is also a practical bridge to heterogeneous Windows hardware.

### 42. Which ONNX version and graph do you use?

**Short answer:** Opset 17, IR version 10, with `MatMul`, `Add`, and `Sigmoid`.

**Deep answer:** The input is float `features` shaped `[batch, 10264]`, and the output is `[batch, 1]`. This simple contract is easy to validate and provider-portable.

### 43. How do you know ONNX did not change predictions?

**Short answer:** FP32 native and ONNX outputs were compared across all 766 test examples with 100% class agreement.

**Deep answer:** Maximum absolute probability difference was `9.242706e-8` and mean difference was `2.269248e-8`. The equivalence report is a versioned artifact.

### 44. Is the quantized model your main model?

**Short answer:** No; FP32 remains the primary reported model.

**Deep answer:** The QDQ candidate is 11,733 bytes and had 99.7389% class agreement against FP32, but its maximum probability difference was 0.119397. It is prepared for accelerator validation rather than substituted into the headline result.

### 45. Did quantization use the test set?

**Short answer:** No; calibration used 300 validation examples.

**Deep answer:** The quantization contract uses QUInt8 activations and QInt8 weights. Keeping test data out of calibration preserves the final comparison’s role.

### 46. What happens if the model file is changed?

**Short answer:** Artifact hashes and runtime checks make model identity visible and gate verified paths.

**Deep answer:** The package and reports bind expected artifacts to SHA-256 values. A production release would extend this with code signing, secure updates, and stronger tamper resistance.

### 47. Can the model batch inputs?

**Short answer:** The ONNX contract has a dynamic batch dimension.

**Deep answer:** The product UI currently analyzes explicit user submissions, but `[batch, 10264]` permits batched evaluation and benchmarking. Product batching would still need latency and memory validation.

### 48. Why not put TF-IDF inside the ONNX graph?

**Short answer:** The current boundary keeps the vocabulary pipeline deterministic and the graph broadly provider-compatible.

**Deep answer:** Text operators can have uneven accelerator support, while dense linear algebra has a simple portable path. The feature contract is hashed and versioned with the model so separation does not mean ambiguity.

## Snapdragon, QNN, and performance

### 49. Is the current demo running on a Snapdragon NPU?

**Short answer:** No; the audited development machine selects `CPUExecutionProvider`.

**Deep answer:** It is AMD64 Windows and exposes Azure and CPU providers, not QNN. The UI and runtime report explicitly mark Snapdragon NPU verification false.

### 50. Then why call it a Snapdragon project?

**Short answer:** Snapdragon is the implemented deployment target, while physical NPU verification is the remaining hardware milestone.

**Deep answer:** The repository includes an ONNX deployment, QDQ candidate, QNN provider path, strict no-fallback gate, hash checks, and runtime truth reporting. We separate architecture readiness from claims that require compatible-device evidence.

### 51. What exactly remains to validate?

**Short answer:** ARM64 packaging, real QNN/HTP execution, strict provider evidence, and device latency/power/thermal measurements.

**Deep answer:** The run must record device and software versions, model hash, provider selection, node assignment where available, prediction equivalence, and fixed-workload benchmarks. Until then, no NPU benefit is claimed.

### 52. How will you prevent silent CPU fallback on Snapdragon?

**Short answer:** The verification path requires QNN selection and rejects a run that cannot prove the intended accelerated execution.

**Deep answer:** Provider availability alone is insufficient. The gate combines provider reporting, strict no-fallback behavior, expected artifact identity, and a captured runtime report.

### 53. Is the QDQ model guaranteed to run on the NPU?

**Short answer:** No; it is NPU-prepared, not device-verified.

**Deep answer:** Operator support, quantization constraints, runtime versions, and provider configuration must all be tested on the target device. The document deliberately avoids equating QDQ export with successful HTP execution.

### 54. Is Snapdragon faster or more efficient here?

**Short answer:** That has not been measured, so we do not claim it.

**Deep answer:** The architectural hypothesis is that the NPU can support efficient local inference, but valid comparison requires a pinned device protocol and instrumentation. Current latency numbers are CPU-only.

### 55. What are the current CPU timings?

**Short answer:** Median full text pipeline is 5.0894 ms and full multimodal is 1,863.35 ms on the audited development machine.

**Deep answer:** ONNX inference alone is 0.0798 ms, TF-IDF is 0.6348 ms, QR decode is 34.418 ms, and cold start is 122.3451 ms. Browser rendering and incident persistence are excluded, and none of these are Snapdragon measurements.

### 56. Why accelerate such a small linear model?

**Short answer:** The current model proves the deployment and verification path; future local pipelines may have heavier OCR or compact semantic stages.

**Deep answer:** For this graph, provider overhead may dominate, so a speed claim would be premature. The value of the architecture is honest heterogeneous execution, with measurement deciding which stages actually benefit from the NPU.

## Privacy and data handling

### 57. Does any submitted content go to the cloud?

**Short answer:** No cloud AI integration is enabled; analysis is through the local service.

**Deep answer:** Messages, URLs, and images stay within the local application pipeline. The project should be re-audited if future integrations introduce networking.

### 58. What is stored after analysis?

**Short answer:** A SHA-256 input hash and sanitized decision metadata.

**Deep answer:** Records can include timestamp, input type, category, score, severity, processing time, provider, model version, and sanitized indicator names. Raw source, screenshots, full URLs, passwords, tokens, and extracted PII are excluded.

### 59. Why store an input hash?

**Short answer:** It supports local correlation without retaining the submitted content.

**Deep answer:** A hash can identify repeated identical input for operational history, but it is still metadata and may be vulnerable to guessing for predictable text. Users can delete records, and high-assurance deployments could disable or key that field.

### 60. Is process memory perfectly private?

**Short answer:** No; local processing reduces exposure but does not defeat a compromised endpoint.

**Deep answer:** An attacker with sufficient local privileges could inspect memory, modify artifacts, or intercept UI input. SnapShield minimizes persistence; it does not replace operating-system isolation and endpoint security.

### 61. How is PII handled?

**Short answer:** Sensitive patterns are detected locally and displayed in redacted form by default.

**Deep answer:** The result includes masked finding types and redacted text, while extracted PII is not written into incident history. Pattern detection can still miss novel formats or flag test-like values.

### 62. Can a user delete history?

**Short answer:** Yes; individual incidents and the entire local history can be deleted.

**Deep answer:** The Incident center exposes both controls. Production retention policies would need secure deletion expectations and administrator/user governance.

### 63. Is there telemetry?

**Short answer:** The documented application does not require cloud AI or remote content telemetry.

**Deep answer:** Runtime and benchmark reports are generated locally. Any future diagnostics must be explicit, minimized, and separate from source content.

### 64. Why is local better than encrypted cloud processing?

**Short answer:** It removes routine third-party transfer and remains available offline, though it does not make the endpoint invulnerable.

**Deep answer:** Encryption in transit protects a channel, not necessarily server-side processing, retention, subpoenas, or account compromise. Local-first narrows the data boundary, while endpoint hardening remains essential.

## Engineering, testing, and packaging

### 65. How much automated testing exists?

**Short answer:** The verified state has 77 passing backend tests plus passing frontend lint, strict TypeScript, production build, and dependency audits.

**Deep answer:** Tests cover API behavior, security constraints, model/runtime contracts, privacy-safe incident handling, demo assets, and related invariants. Passing tests improve confidence but are not proof of absence of vulnerabilities.

### 66. Is the packaged app signed?

**Short answer:** No; the current AMD64 executable reports `NotSigned`.

**Deep answer:** It is a verified competition package, not a production-distribution claim. Code signing, reputation, and secure update infrastructure are roadmap requirements.

### 67. What package did you verify?

**Short answer:** A 372.28 MiB AMD64 package with 1,363 files and a recorded executable SHA-256.

**Deep answer:** The executable hash is `a3d07328f3f2a6d8b03a1bdb24ed8d800e59661330d32b941538bc74b2248036`. Its manifest and real evaluator-flow capture bind the deliverable to the audited artifacts.

### 68. Why is the package so much larger than the model?

**Short answer:** It bundles the desktop/runtime environment, Python service, OCR and imaging dependencies, frontend assets, and models.

**Deep answer:** The 41 KB ONNX graph is only one artifact. RapidOCR, OpenCV, application runtimes, and packaging overhead dominate the 372.28 MiB build.

### 69. What happens offline?

**Short answer:** Core analysis continues because the model, rules, OCR, QR decoder, and storage are local.

**Deep answer:** No reputation lookup or cloud AI is required. Offline operation also means no fresh threat-intelligence feed, which is an explicit tradeoff.

### 70. How do you guard image uploads?

**Short answer:** The API restricts type and size and decodes supported PNG, JPEG, or WEBP images locally.

**Deep answer:** The UI limit is 10 MB, and tests cover input constraints. Production hardening should add continued fuzzing, library patching, resource limits, and sandbox review.

### 71. Are the demo attacks real?

**Short answer:** No; they are safe synthetic samples.

**Deep answer:** They use reserved `.example` domains, the documentation address `192.0.2.1`, a standard test card number, and an explicitly fake password. The demo never needs a live malicious destination.

### 72. How do you know the package contains the evaluated model?

**Short answer:** The build manifest and SHA-256 checks connect package contents to the approved artifacts.

**Deep answer:** Runtime reports expose model identity, and the executable/package manifests are retained. A signed production supply chain would strengthen this further.

## Competition, alternatives, and roadmap

### 73. Why not just use Microsoft Defender?

**Short answer:** Defender is a broad security platform; SnapShield is a privacy-first explanatory workflow for user-submitted multimodal content.

**Deep answer:** The products are complementary. SnapShield’s differentiators are explicit local evidence analysis, screenshot/QR correlation, redaction, and sanitized decision history—not a claim to replace endpoint protection.

### 74. Why not VirusTotal?

**Short answer:** VirusTotal is valuable reputation and sample intelligence, while SnapShield avoids uploading sensitive user evidence or contacting a cloud service.

**Deep answer:** A URL hash or sanitized indicator could become an optional consented integration later. The current design intentionally works without disclosing the source content to third parties.

### 75. What stops a major vendor from copying this?

**Short answer:** The defensible value is the integrated local workflow, verified privacy contract, evidence quality, and deployment discipline—not one secret algorithm.

**Deep answer:** Sustainable differentiation would come from trusted evaluation data, device optimization, enterprise policy integration, distribution, and rapid threat adaptation. The competition build demonstrates the technical foundation.

### 76. What would you build next with one week?

**Short answer:** Complete ARM64 packaging and run the strict QNN validation protocol on a real Snapdragon PC.

**Deep answer:** That closes the largest claim gap. I would capture provider, hash, node-placement, equivalence, and fixed-workload performance evidence before changing the model or adding features.

### 77. What would you build next with three months?

**Short answer:** Broader product-level evaluation, signed delivery, and a security/privacy hardening review.

**Deep answer:** The priority is licensed current data across messages, email, screenshots, QR lures, languages, and benign hard negatives, followed by calibrated thresholds and subgroup analysis. Only then would integrations expand.

### 78. What is the biggest technical risk?

**Short answer:** Generalization beyond the narrow SMS corpus and finite rules.

**Deep answer:** Modern attacks shift rapidly across channels and languages. The response is not a bigger claim; it is a provenance-controlled evaluation program, abstention/error analysis, and independently tested pipeline stages.

### 79. What is the biggest credibility risk?

**Short answer:** Confusing Snapdragon readiness with verified NPU execution.

**Deep answer:** The project directly mitigates that risk through provider reporting, strict fallback checks, and written claim boundaries. The current build says CPU because that is what the evidence shows.

### 80. Why should this project win?

**Short answer:** It turns a relevant privacy problem into a working, explainable local product and treats technical truth as part of the user experience.

**Deep answer:** SnapShield demonstrates multimodal analysis, deployable ONNX inference, privacy-safe incident handling, reproducible evaluation, robust packaging, and an implemented Snapdragon path without fabricating device results. It is both useful now on CPU and structured for the exact hardware validation needed next.
