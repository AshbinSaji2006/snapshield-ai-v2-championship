# Failure Analysis

Machine-readable record-level categories are in `reports/v2/failure_analysis.json`; message bodies are omitted.

On the UCI test, calibrated Fast Guard made 14 errors (10 FN, 4 FP), concentrated in other/short ambiguous wording plus a few promotion, urgency and prize/financial cases. Deep Guard reduced this to 11 errors (5 FN, 6 FP); its remaining misses were mostly ambiguous, one promotion and one prize/financial lure. The neural model traded five fewer false negatives for two more false positives.

On the external set, Fast Guard made 66 errors (64 FN, 2 FP). Frequent overlapping categories included ambiguous wording (25), urgency (15), bank impersonation (14), URL-heavy content (14) and financial solicitation (12). Deep Guard reduced this to six errors (4 FN, 2 FP): one URL-heavy miss, one urgency miss, two other ambiguous misses and two false positives containing bank-like language.

This evidence justified shipping Deep Guard and rejecting the first low-escalation router. No message-specific test keyword was added to training or scoring after the final-test review.
