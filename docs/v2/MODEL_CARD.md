# Deep Guard model card

## Identity

- Product role: Deep Guard text-risk signal inside SnapShield AI v2.
- Selected candidate: BERT Tiny L2/H128.
- Upstream: `google/bert_uncased_L-2_H-128_A-2`, revision `30b0a37ccaaa32f332884b96992754e246e48c5f`.
- Upstream/model license: Apache-2.0.
- Deployment version: `deep-guard-bert-tiny-1.0`.
- Runtime: ONNX Runtime; verified provider `CPUExecutionProvider`.
- Maximum sequence length: 128; opset 17; inputs `[1,128]` `input_ids` and `attention_mask`; output `logit`.

## Intended use

Deep Guard supplies a calibrated spam/smishing-like message signal when adaptive routing identifies uncertainty or high-risk context. It is not an autonomous malware detector, universal phishing detector, URL reputation service, or final risk probability. Deterministic evidence and bounded fusion control the user-facing decision.

## Selection

Three candidates were evaluated before final test access. The frozen policy selected the lowest-latency/smallest model within 0.01 of the best recall-weighted validation score. BERT Tiny met that window and had a 17,515,277-byte FP32 ONNX model versus 90,341,665 bytes for MiniLM and 265,522,903 bytes for DistilBERT.

## Evaluation

| Dataset | N | Accuracy | Precision | Recall | F1 | Macro F1 | FPR | FNR |
|---|---:|---:|---:|---:|---:|---:|---:|---:|
| UCI untouched test | 766 | 98.56% | 93.41% | 94.44% | 93.92% | 96.55% | 0.89% | 5.56% |
| 2022 Mendeley-derived independent holdout | 521 | 98.85% | 99.01% | 98.04% | 98.52% | 98.79% | 0.63% | 1.96% |

The external holdout was strictly filtered against the entire UCI corpus and not used for training. Adaptive v2.2 was redesigned after an earlier external-policy failure, so its cross-domain routing result is not described as pristine independent policy validation.

These are named SMS dataset measurements, not universal phishing accuracy or safety guarantees.

## Calibration and equivalence

- Temperature: `2.0088757362936236`, selected on validation data.
- FP32 ONNX class agreement: 100% across 766 UCI test samples.
- Maximum FP32 framework/ONNX probability delta: `0.000001738962864372695`.
- Static QDQ candidate: INT8 MatMul/Gemm, calibrated on 256 validation records.
- QDQ agreement: 100% FP32 class agreement on UCI and external holdouts.
- Maximum QDQ/FP32 UCI probability delta: `0.032188765520130946`.

## Artifact hashes

- FP32 ONNX: `71a4a43e36f5ef23845e28953b0a05785f6bf71c1785680f531e70efefe33f3f`
- QDQ ONNX: `ce1128853b3a399d97d917e0d5bdde51f26b60d816171b3bb8f9732b63cf7827`
- Tokenizer: `da0e79933b9ed51798a3ae27893d3c5fa4a201126cef75586296df9b4d2c62a0`

## Limitations

Training/evaluation data is short-form English SMS. Code-mixed, multilingual, long-form email, visual layout, novel evasion, and business-email compromise are not comprehensively measured. The model may be confidently wrong. Users must independently verify credential and financial requests.

## Snapdragon status

The QDQ candidate and strict QNN workflow are implemented. QNN/Snapdragon NPU execution is not verified because compatible hardware and configured AI Hub authentication are unavailable. No NPU performance or power claim is approved.
