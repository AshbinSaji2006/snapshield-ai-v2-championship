# Risk Calibration

Classifier probabilities and SnapShield's final risk score are deliberately separate.

Fast Guard uses Platt scaling fitted on five-fold out-of-fold predictions from the combined train+validation development data. For an honest calibration audit, a temporary calibrator was fit on one stratified half of the OOF predictions and evaluated on the other half: Brier score improved from 0.01392 to 0.01266 and 10-bin ECE from 0.02351 to 0.00559. Macro F1 changed from 96.29% to 96.10%; recall increased from 89.37% to 90.16%. The deployment calibrator was then fit on all OOF predictions. The final test was not used.

Deep Guard uses temperature scaling from its dedicated 383-message validation calibration partition. BERT Tiny temperature is 2.00888. Its disjoint selection-partition Brier score improved from 0.01051 to 0.01025 and ECE from 0.01057 to 0.00499 without changing the fixed 0.5 class boundary.

The UI labels model values as message-class probabilities. The 0–100 final risk score remains an ordinal, evidence-weighted security index; it is never described as a probability of maliciousness.
