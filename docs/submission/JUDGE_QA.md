# Judge Q&A

1. **Why does this require AI?** Social-engineering language varies too widely for exact rules alone. A learned TF-IDF/logistic classifier generalizes vocabulary patterns, while deterministic engines cover high-value structure and make decisions inspectable.
2. **Why Snapdragon?** Private screenshots/messages benefit from local inference and offline availability. The small ONNX/QDQ boundary is designed for efficient QNN HTP deployment, but target performance still requires hardware validation.
3. **Why not cloud AI or ChatGPT?** They introduce a disclosure boundary and generative variability. SnapShield is offline and evidence-led; no LLM makes security decisions.
4. **Why not VirusTotal or Google Safe Browsing?** Reputation services are valuable but share indicators, require connectivity, and may not know a novel/private lure. SnapShield deliberately performs local content and structural analysis and could complement, not replace, opt-in reputation.
5. **Why not Microsoft Defender?** Defender is broader endpoint protection. SnapShield specializes in explainable message, screenshot, QR, URL, and PII decision support. It is not antivirus.
6. **How does the classifier work?** Lowercased word unigrams/bigrams become 10,264 TF-IDF features. Logistic regression outputs a spam probability; that is one signal in risk fusion.
7. **Which dataset?** UCI SMS Spam Collection, DOI 10.24432/C5CC84, CC BY 4.0: 5,574 original and 5,105 retained after deduplication.
8. **How did you prevent leakage?** Exact and normalized near-duplicate removal happened before the seed-42 stratified 70/15/15 split. Selection used validation only; final test was touched once.
9. **What are the split sizes?** Train 3,573, validation 766, untouched test 766. Final retraining used train+validation.
10. **Which alternatives were evaluated?** Word TF-IDF/logistic, char TF-IDF/logistic, and char TF-IDF/LinearSVC. Selection considered recall, macro F1, FPR, size, latency, and ONNX suitability.
11. **Why no transformer?** No licensed task-specific checkpoint was available offline, a generic transformer would materially increase dependencies/deployment cost, and this small corpus did not justify it. We make no claim that transformers would perform worse.
12. **What is test accuracy?** 98.17% on the named 766-message UCI test split, not a universal phishing-accuracy claim.
13. **Precision, recall, and F1?** Spam precision 97.50%, recall 86.67%, and F1 91.76%; macro F1 95.37%.
14. **FPR and FNR?** FPR 0.296% (2/676 ham); FNR 13.33% (12/90 spam). The FNR is why ML is never the sole authority.
15. **ROC/PR?** ROC-AUC 0.9928 and average-precision PR-AUC 0.9722 on that test split.
16. **Why is the risk score trustworthy?** It is traceable, not probabilistically guaranteed. Each contribution has a stable ID and evidence; single findings are discounted and severity bands are regression-tested.
17. **What is heuristic versus learned?** Spam probability is learned. URL structure, text patterns, Unicode evasion, brand mapping, PII, QR routing, weights, thresholds, explanations, and recommendations are deterministic heuristics/policy.
18. **Is an LLM involved?** No. No generative model or cloud call exists in the decision path.
19. **How does OCR work?** RapidOCR uses local ONNX Runtime models after Pillow validates bytes, format, and decoded dimensions. It returns extracted lines, mean confidence, and timing.
20. **How does QR work?** OpenCV decodes pixels locally. URL/text payloads enter the same analyzers and are never opened.
21. **What data leaves the machine?** None during analysis. Dataset download is a separate explicit training step from official UCI.
22. **What does SQLite store?** Input hash, timestamp, type, score, severity, classification, category, provider, latency, model version, and sanitized signal metadata. No raw message, image, full URL, or secret.
23. **Can it work offline?** Yes after dependencies/models are installed; the production UI has no CDN/font dependency.
24. **Is Snapdragon NPU really running?** No. This machine is Intel/AMD64 and the selected provider is `CPUExecutionProvider`.
25. **What exactly is Snapdragon-ready?** A verified numeric ONNX graph, calibrated QDQ candidate, runtime provider gate/fallback, exact operator/input contract, and automated validation report/script.
26. **How would QNN deployment be proven?** On native ARM64, enumerate QNN EP, disable CPU fallback, verify all-node assignment and outputs, then benchmark identical inputs and record the exact SoC/runtime/profile.
27. **Which ONNX operators?** FP32 uses `MatMul`, `Add`, `Sigmoid`; the quantized candidate adds Q/DQ nodes around the linear layer.
28. **Why QNN?** It is the ONNX Runtime provider for Qualcomm backends, including HTP, and preserves a provider-based application boundary.
29. **What happens if QNN fails?** Initialization falls back to another available provider/CPU; if ONNX itself fails, the local serialized scikit-learn model is used.
30. **How much faster is NPU than CPU?** Unknown and intentionally not estimated. No Snapdragon/QNN run was available.
31. **What CPU latency is measured?** Median warm ONNX-only 0.0798 ms, TF-IDF 0.6348 ms, full text 5.0894 ms, QR 34.418 ms, and full OCR+QR+security 1863.35 ms on this development PC.
32. **Is ONNX output correct?** Across all 766 test records, FP32 class agreement with scikit-learn was 100%; max probability difference was `9.24e-8`.
33. **Is QDQ production-ready?** Not yet. It is 11,733 bytes and reached 99.739% class agreement versus FP32, but full HTP assignment/correctness must be verified without CPU fallback.
34. **Does it browse suspicious links?** Never. It performs no DNS, HTTP, redirect expansion, or navigation.
35. **How is brand impersonation detected?** A controlled small map of high-quality official domains compares mentioned brands with observed hostnames. It is labeled heuristic, not an exhaustive brand registry.
36. **How are obfuscations handled?** Tests cover `hxxp`, bracketed dots, zero-width characters, mixed Latin/Cyrillic/Greek scripts, spaced `p a s s w o r d`, IP/punycode/`@` URLs, nested subdomains, and brand names in paths.
37. **Could a legitimate security notice be flagged?** Yes. Protective advice is recognized to suppress obvious credential-rule false positives, but contextual errors remain. Users are told to verify independently.
38. **How is input safely displayed?** React escapes text; no unsafe HTML insertion is used. CSP and security headers add defense in depth.
39. **What prevents SQL injection?** Parameterized SQLite statements. Source input is not used to construct SQL.
40. **What prevents hostile localhost access?** Loopback binding, trusted hosts, local-origin enforcement, restricted CORS, JSON requests, and security headers. A production desktop shell should add a per-launch token.
41. **How are image bombs handled?** 10 MiB compressed size and 25-megapixel decoded size caps plus MIME/format validation and Pillow verification before OCR/QR.
42. **What tests pass?** 77 backend tests including real OCR and QR, ONNX/fallback/exact QNN artifact gating, API/database/security/adversarial behavior; frontend lint, strict typing, build, and audit also pass.
43. **What is the adversarial result?** 18/18 curated cases land in expected bands, but it is a small functional regression suite and is not reported as accuracy.
44. **Is the Windows app packaged?** Yes: a smoke-tested 372.28 MiB AMD64 one-folder artifact. It is explicitly unsigned and not an installer.
45. **Biggest model limitation?** English, older SMS data and 13.33% spam FNR; broader modern, multilingual, email, and screenshot corpora are needed.
46. **Biggest Snapdragon limitation?** No actual ARM64/QNN HTP run, so there is no verified NPU latency, speedup, or power result.
47. **What would be required to ship?** Broader/current validation, rate limiting and per-launch authentication, signed ARM64 packaging/updater, target QNN qualification, formal accessibility review, dependency governance, and operational false-positive monitoring.
