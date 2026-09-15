# v1 vs v2 Competition Scorecard

| Dimension | v1 frozen fallback | v2 championship | Decision |
|---|---|---|---|
| ML depth | TF-IDF logistic Fast model | Fast Guard + selected/calibrated BERT Tiny Deep Guard | v2 stronger |
| UCI positive recall | 86.67% original uncalibrated release metric | 94.44% Deep/Adaptive under v2 evaluation | v2 stronger |
| External robustness | No independent cross-domain report | 521-record deduplicated Mendeley evaluation; Deep recall 98.04% | v2 stronger |
| Adaptive compute | None | Explicit route classes/reasons; Deep on 33.68% UCI and 51.25% external | v2 stronger |
| Normalization | Limited | Separate original/security views, zero-width, confusable, defanged/spaced URL handling | v2 stronger |
| Domain intelligence | Heuristic host strings | Offline PSL, registrable domain, IDNA and mixed-script facts | v2 stronger |
| Explainability | Flat evidence list | Flat evidence plus machine-readable interactive Threat Evidence Graph | v2 stronger |
| Proactive mode | None | Off-by-default, consented Live Shield | v2 stronger |
| Snapdragon evidence | CPU verified; QNN pending | Exact Deep QDQ artifact + AI Hub compile/profile workflow; still pending auth | improved readiness, same hardware status |
| Local text latency | v1 full pipeline 5.09 ms on earlier build | v2 final run: Fast 1.16 ms; Deep 10.42 ms; full deep-routed sample 28.69 ms | v1 faster; v2 more capable |
| OCR | Local RapidOCR | Same pipeline with bounded ORT threads; still slow on current CPU | tie / known limitation |
| Tests | 77 backend | 100 backend plus v2 security/runtime/Live/graph tests | v2 stronger |
| UX/demo | Polished single-result UI | Adaptive route, graph explorer, Live Shield and guard/runtime states | v2 stronger |
| Stability fallback | Frozen tagged v1 package | v2 separate branch/artifacts | v1 retained as fallback |

Verdict: v2 is the stronger competition candidate. Its source gates, AMD64 package build, and packaged health/Deep-Guard smoke test pass. v1 remains an immutable fallback because v2 has a larger dependency/package surface and the Snapdragon hardware path remains unverified.
