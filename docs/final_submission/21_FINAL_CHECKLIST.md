# Final Competition Checklist

Legend: `[x]` completed and verified in the repository; `[ ]` requires the submitter or access to external hardware/platforms.

## Canonical truth

- [x] One canonical fact sheet exists at `SUBMISSION_FACTS.md` and `01_PROJECT_FACTS.md`.
- [x] Dataset source, DOI, license, access date, hash, row counts, split, and duplicate policy are stated consistently.
- [x] Classifier metrics are scoped to the fixed retained UCI SMS test split.
- [x] ONNX FP32 and QDQ results are clearly separated.
- [x] CPU benchmark numbers are labeled as development-machine measurements.
- [x] Current provider is stated as `CPUExecutionProvider`.
- [x] QNN readiness is separated from verified Snapdragon NPU execution.
- [x] Package size, architecture, signature state, and executable hash are recorded.

## Submission package

- [x] Elevator pitches and 50/100/150/250/500-word descriptions are prepared.
- [x] Eight-slide deck plus 5-minute, 3-minute, and 90-second scripts are prepared.
- [x] Architecture and privacy graphics are rendered at 1920 × 1080; Mermaid source remains available.
- [x] Eight real packaged-application screenshots are captured and verified at 1920 × 1080.
- [x] Final presenter script, 3:35 demo narration, and exact real-screen recording guide are prepared.
- [x] Judge-facing release directory, internal checksum manifest, competition ZIP, and external SHA-256 manifest are prepared.
- [x] Current public competition deadline/rules were checked on 2026-09-13; authenticated upload formats and limits remain a submission-day check.
- [x] Portal answers, asset map, recording run sheet, video QA checklist, presentation card, and submission-day checklist are prepared.
- [x] Exact live demo, safe inputs, failure recovery, and screenshot plan are prepared.
- [x] Submission-form answers and impact/differentiation matrix are prepared.
- [x] Technical, metrics, Snapdragon, limitations, and roadmap defenses are prepared.
- [x] Final judge Q&A contains 80 questions with short and deep answers.
- [x] README links to the canonical submission package.
- [x] A top-level quick-start guide exists.

## Verified engineering state

- [x] Backend suite: 77 tests passing.
- [x] Frontend lint: passing.
- [x] Strict TypeScript check: passing.
- [x] Frontend production build: passing.
- [x] Python and npm dependency audits: passing in the recorded project state.
- [x] FP32 ONNX equivalence: 766/766 class agreement.
- [x] Packaged AMD64 smoke test: passing.
- [x] Demo inputs use safe synthetic content.
- [x] No model, dataset, risk, security logic, benchmark method, API, or ONNX artifact changed; only the documented result-visibility and loopback packaged-UI blockers were corrected.

## Human capture and submission tasks

- [ ] Create a read-only backup/tag of the final repository state.
- [ ] Replace the repository URL placeholder in the submission form with the public URL.
- [ ] Confirm the public repository contains no credentials, personal data, private paths, local databases, or unintended build artifacts.
- [x] Render and inspect architecture/privacy graphics at slide resolution.
- [x] Build and visually inspect the eight-slide 16:9 deck.
- [x] Capture and inspect all eight screenshots from the actual packaged build at 1920 × 1080.
- [ ] Record a clean 1080p local demo; disclose the visible provider accurately.
- [x] Export the deck through PowerPoint to PDF and verify fonts, image crops, contrast, and PPTX/PDF synchronization.
- [x] Assemble the offline evidence pack in `release/final_submission/` with real screenshots, visuals, scripts, summary, and answers.
- [ ] Rehearse the 5-minute script to a timer at least three times.
- [ ] Rehearse the 3-minute and 90-second fallbacks.
- [ ] Test the packaged app and video on the exact presentation laptop, display adapter, and screen resolution.
- [ ] Disable notifications, updates, sleep, and screen savers before presenting.
- [ ] Confirm the laptop is powered and the backup copy is offline-accessible.
- [ ] Run the platform’s submission preview and inspect line breaks and character limits.
- [ ] Confirm licenses and third-party notices are visible in the public repository.
- [ ] Submit before the deadline and preserve the confirmation receipt.

## Only if compatible Snapdragon hardware becomes available

- [ ] Follow the protocol in `17_SNAPDRAGON_DEFENSE.md` without modifying the benchmark after viewing results.
- [ ] Capture unedited QNN/HTP provider evidence, exact model hash, environment versions, and no-fallback status.
- [ ] Compare device predictions against the approved FP32 reference.
- [ ] Report device latency/power/thermal numbers only with a documented method.
- [ ] Update every claim-bearing document together; otherwise retain the current “unverified” language.

## Final five-minute gate

- [x] Project title and subtitle match the form, deck, video script, README, and fact sheet.
- [x] “98.17%” is immediately qualified as a retained UCI SMS test-split result.
- [x] No slide says or visually implies verified Snapdragon NPU execution.
- [ ] The live provider badge is visible during the demo.
- [x] Every screenshot is from the actual build, not a mockup.
- [x] Demo URLs remain inert and no real PII or credential is shown.
- [x] The first spoken sentence states the user problem; the final sentence states the measurable next milestone.
