# SnapShield AI v2 — championship judge Q&A

Answers are intentionally short enough for live delivery. Expand only when asked.

## Product and problem

1. **What is SnapShield AI?** A local-first multimodal cyber-defense copilot for messages, URLs, screenshots, and QR codes.
2. **What problem does it solve?** It helps users inspect suspicious content without requiring a cloud AI round trip.
3. **Why does privacy matter here?** The suspicious content may itself contain banking, identity, or authentication information.
4. **Is it just a spam classifier?** No. Text ML is one signal alongside URL, OCR, QR, PII, brand/domain, rule, graph, and action layers.
5. **Who is it for?** People and small teams who need understandable, local checks before they click, reply, pay, or disclose data.
6. **What inputs are supported?** Messages, URLs, PNG/JPEG/WEBP screenshots, and QR-containing images.
7. **What does the user receive?** An ordinal risk, severity, evidence trail, explanation, and recommended action.
8. **Does SnapShield block threats automatically?** No. It advises the user; it does not silently delete content or navigate destinations.
9. **What is the core product promise?** Your data never needs to leave your device to protect your device.
10. **What makes the demo memorable?** A screenshot becomes OCR text, a decoded QR destination, connected evidence, and an explainable action.

## Local processing and privacy

11. **Does analysis call a cloud AI API?** No. The core inference and security engines run locally after installation.
12. **Does it visit submitted URLs?** No. It parses and scores their structure without navigation, DNS lookup, or payload execution.
13. **What is stored in incident history?** Content hashes, risk and derived sanitized metadata—not raw submitted messages or images.
14. **Is no data ever written anywhere?** Submitted raw source is excluded from incident history; normal OS/runtime behavior and user-controlled files still exist.
15. **Can the user redact PII?** Yes. The interface detects supported PII patterns and provides a masked representation.
16. **Is Live Shield always watching?** No. It is off by default and requires explicit consent.
17. **What does Live Shield inspect?** Newly copied text while enabled, subject to deduplication and rate limits.
18. **Does Live Shield automatically save alerts?** No. Alerts are volatile unless the user explicitly saves an incident.
19. **Does local mean perfectly private?** No. Endpoint compromise, screen capture, and OS-level access remain outside the app’s boundary.
20. **Why say ‘may require remote processing’ about cloud tools?** It is accurate without claiming every competing system uploads every input.

## Machine learning

21. **What is Fast Guard?** The calibrated v1 TF-IDF logistic classifier exported to ONNX.
22. **What is Deep Guard?** A compact BERT Tiny L2/H128 text model deployed as FP32 ONNX.
23. **Why two models?** Extreme-confidence cases can stay fast while ambiguous or contextual cases receive deeper analysis.
24. **How was Deep Guard chosen?** Three candidates were compared under a frozen validation policy; within 0.01 of the best score, latency then size decided.
25. **Which candidates were tested?** BERT Tiny, MiniLM, and DistilBERT variants documented in the tournament report.
26. **Why did BERT Tiny win?** It met the validation-quality tolerance with substantially lower latency and artifact size.
27. **Was the test set used to select it?** No. Candidate selection was completed from development/validation evidence before test evaluation.
28. **How was Fast Guard calibrated?** Platt calibration fitted to development-only out-of-fold predictions.
29. **Did calibration read the test labels?** No. Its approval gate used development-only out-of-fold evidence.
30. **Is the risk score a probability?** No. Final risk is a bounded expert-policy ordinal score; model probability is only one evidence input.

## Adaptive routing

31. **What triggers Deep Guard?** Non-extreme Fast probability, entropy, and contextual security triggers under the documented v2.2 policy.
32. **How often does it escalate on UCI?** 33.68% of the 766-message test.
33. **How often on the external holdout?** 51.25% of 521 messages.
34. **Why is external escalation higher?** Domain shift creates more uncertainty and contextual triggers.
35. **Does routing preserve UCI recall?** Yes. Adaptive v2.2 matches Deep Guard’s 94.44% positive recall there.
36. **What is the UCI adaptive FPR?** 0.30%, specifically 2 false positives among 676 negative test messages.
37. **Was there a failed router?** Yes. v2.1 under-escalated external threats and is retained as a rejected report.
38. **Was v2.2 a pristine independent-policy result?** No. It was redesigned after observing v2.1’s cross-domain failure, and that limitation is disclosed.
39. **Why keep the rejected report?** It prevents selective-history erasure and shows the engineering correction.
40. **Can users see routing decisions?** Yes. The response includes the route, decision class, and reason codes.

## Data protocol

41. **What is the primary dataset?** The UCI SMS Spam Collection under CC BY 4.0.
42. **How many UCI messages remain after deduplication?** 5,105.
43. **How large is the untouched UCI test?** 766 messages.
44. **What is the external dataset?** A 2022 Mendeley SMS spam/smishing dataset under CC BY 4.0.
45. **How large is the retained external holdout?** 521 messages: 317 ham, 87 spam, and 117 smishing.
46. **Why only 521 external records?** Strict exact/near UCI-overlap removal and deterministic cleaning exclude contamination or ambiguity.
47. **Was external data used to train Deep Guard?** No. It is an evaluation holdout.
48. **Are dataset hashes recorded?** Yes. Source, processed split, and deployed artifacts have SHA-256 provenance.
49. **Why use an older UCI corpus?** It provides a reproducible public baseline, while the external 2022 holdout probes more recent domain shift.
50. **Do these datasets represent all phishing?** No. They are SMS datasets and cannot establish universal phishing performance.

## Results

51. **What is Deep Guard UCI accuracy?** 98.56% on the 766-message untouched test.
52. **What is Deep Guard UCI recall?** 94.44% for the positive class.
53. **What is Deep Guard UCI FPR?** 0.89%.
54. **What is Deep Guard external accuracy?** 98.85% on the 521-message deduplicated holdout.
55. **What is Deep Guard external recall?** 98.04%.
56. **What is Deep Guard external FPR?** 0.63%.
57. **How does Fast Guard transfer externally?** Its recall falls to 68.63%, which demonstrates meaningful domain shift.
58. **What is Adaptive v2.2 UCI accuracy?** 99.09%.
59. **What is Adaptive v2.2 UCI macro F1?** 97.76%.
60. **What is the functional evaluation result?** 20 of 20 expert-curated robustness cases pass; this is coverage, not accuracy.

## ONNX and runtime

61. **What inference runtime is used?** ONNX Runtime.
62. **What provider is verified on this machine?** `CPUExecutionProvider`.
63. **Is AzureExecutionProvider available?** It may be enumerated by the environment, but the deployed model selected CPUExecutionProvider.
64. **Does the UI report the actual provider?** Yes. Runtime state comes from live provider selection.
65. **What is FP32 agreement?** The deployed FP32 ONNX classifier matched reference class decisions across all 766 UCI samples.
66. **What is the QDQ artifact?** A statically quantized candidate intended for strict QNN validation.
67. **How was QDQ checked?** It preserved 100% FP32 class agreement on both named holdouts.
68. **Does QDQ agreement prove NPU execution?** No. It proves model-output agreement, not QNN assignment or hardware execution.
69. **What is the median full deep-routed timing?** 28.69 ms on the current AMD64 development CPU in the final benchmark run.
70. **Is that a Snapdragon number?** No. No Snapdragon latency or energy measurement is claimed.

## Snapdragon and QNN

71. **Does it run on a Snapdragon NPU today?** That has not been verified in this environment.
72. **What Snapdragon wording is safe?** “Designed for Snapdragon-powered PCs” and “QNN hardware validation pending.”
73. **What has actually been implemented?** Provider abstraction, strict QNN selection, QDQ candidate, hash gate, and AI Hub automation.
74. **Why use an exact-artifact gate?** A hardware claim is accepted only for the same compiled artifact whose hash was validated.
75. **Does CPU fallback count as QNN success?** No. The strict validation path disables silent CPU fallback.
76. **What hardware target is configured?** Qualcomm AI Hub’s Snapdragon X Elite CRD target.
77. **Why is validation pending?** This machine lacks compatible Snapdragon Windows ARM64 hardware/QNNExecutionProvider and AI Hub credentials are not configured.
78. **What evidence will complete validation?** Compile/profile/inference job IDs, device/runtime metadata, raw logs, artifact hash, numerical check, and verified QNN assignment.
79. **Are energy savings claimed?** No. Potential efficiency is an architectural motivation, not a measured result.
80. **Why is Snapdragon relevant anyway?** The workload is local, privacy-sensitive, continuous-capable inference with an explicit portable-to-QNN deployment boundary.

## Multimodal and explainability

81. **Which OCR engine is used?** RapidOCR running locally through ONNX Runtime.
82. **Which QR engine is used?** OpenCV `QRCodeDetector` locally.
83. **Can decoded QR URLs open automatically?** No. They are displayed and structurally analyzed only.
84. **What is the Threat Evidence Graph?** A machine-readable set of evidence nodes and relationships used for inspection and fusion.
85. **Why a graph instead of a flat list?** It exposes relationships such as claimed brand, observed domain, decoded URL, and conflicting expected domain.
86. **What is brand/domain mismatch?** A claimed supported brand linked to a destination outside its known official domain family.
87. **How is Unicode evasion handled?** Original and normalized representations are preserved, with bounded confusable and IDNA evidence.
88. **What India-focused patterns exist?** Documented rules cover examples such as digital arrest, KYC, UPI refund, electricity, customs, and job-fee lures.
89. **Are those rules a learned India-wide model?** No. They are transparent, limited expert rules.
90. **Can an explanation be wrong?** Yes. Heuristics and models can miss or over-weight evidence; limitations and safe user actions remain visible.

## Security, delivery, and roadmap

91. **How is untrusted image input handled?** Size/type limits and defensive decode precede OCR/QR analysis.
92. **Can API callers submit unlimited content?** No. Request and image size bounds are tested.
93. **Is stored output safe for the UI?** React escaping and structured response handling are tested, including hostile markup strings.
94. **Are dependencies vulnerability-free forever?** No. Current Python and npm audits found no known advisories at the recorded time; future audits remain necessary.
95. **How many backend tests pass?** 100.
96. **Is the Windows build signed?** No. It is an unsigned AMD64 one-folder build and must be labeled as such.
97. **Is native Windows ARM64 packaging complete?** No. The ARM64 build procedure is documented and requires the target environment.
98. **What are the largest current limitations?** Named-data scope, heuristic URL/brand coverage, OCR variability, no live reputation, and pending QNN hardware proof.
99. **What is the next engineering milestone?** Run the strict AI Hub/compatible-device validation workflow and publish only the resulting measured evidence.
100. **Why should this project win?** It is a working, privacy-first product with real multimodal analysis, honest cross-domain evidence, interpretable routing, and unusually disciplined hardware claims.

## Alternatives and differentiation

101. **Why not Microsoft Defender?** SnapShield is a user-facing evidence copilot for content a person is evaluating; it complements rather than replaces endpoint antivirus and platform protection.
102. **Why not SmartScreen?** SmartScreen focuses on reputation and downloaded/web content; SnapShield correlates submitted text, OCR, QR, brand/domain, PII, and social-engineering evidence locally.
103. **Why not Google Safe Browsing?** Reputation services are valuable but require a remote lookup and may lack the surrounding message/image context; SnapShield intentionally provides offline structural analysis.
104. **Why not VirusTotal?** Uploading a private message or screenshot to a multi-engine service changes the privacy boundary; SnapShield’s core workflow stays on device.
105. **Why not paste it into ChatGPT?** That may disclose sensitive content to a remote AI workflow; SnapShield is purpose-built, bounded, local, and exposes deterministic evidence.
106. **Is the graph a graph neural network?** No. It is an explainability/provenance data structure, not a learned GNN.
107. **Can domain mismatch create false positives?** Yes. Legitimate delegates and unfamiliar official domains exist, so the UI says “does not match the finite expected-domain map,” not “proven malicious.”
108. **Can attackers bypass OCR?** Yes. Distortion, layout, language, or image quality can defeat OCR, which is why OCR is one fallible signal and low risk is not a safety guarantee.
109. **How is Hinglish handled?** Transparent rules cover selected Romanized Hindi/Hinglish cases, reported only as functional robustness—not multilingual accuracy.
110. **What does SnapShield replace?** It replaces none of Defender, browser reputation, institutional fraud controls, or user verification; it adds a private local evidence layer before action.
