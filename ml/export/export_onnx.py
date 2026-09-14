"""Export the numeric linear classifier to ONNX and validate CPU agreement."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
from pathlib import Path

import joblib
import numpy as np
import onnx
import onnxruntime as ort
from onnx import TensorProto, helper, numpy_helper
from onnxruntime.quantization import CalibrationDataReader, QuantFormat, QuantType, quantize_static

ROOT = Path(__file__).resolve().parents[2]
ARTIFACT_DIR = ROOT / "ml" / "artifacts"
DATA_DIR = ROOT / "data" / "processed" / "uci_sms"
OPSET = 17


class FeatureCalibrationReader(CalibrationDataReader):
    def __init__(self, features: np.ndarray):
        self._items = iter([{"features": row[None, :]} for row in features])

    def get_next(self):
        return next(self._items, None)


def export() -> Path:
    vectorizer = joblib.load(ARTIFACT_DIR / "text_vectorizer.joblib")
    classifier = joblib.load(ARTIFACT_DIR / "text_classifier.joblib")
    feature_count = len(vectorizer.vocabulary_)
    weight = classifier.coef_.astype(np.float32).T
    bias = classifier.intercept_.astype(np.float32)
    graph = helper.make_graph(
        [helper.make_node("MatMul", ["features", "weight"], ["logit_matmul"]), helper.make_node("Add", ["logit_matmul", "bias"], ["logits"]), helper.make_node("Sigmoid", ["logits"], ["probability"])],
        "snapshield_text_classifier",
        [helper.make_tensor_value_info("features", TensorProto.FLOAT, [None, feature_count])],
        [helper.make_tensor_value_info("probability", TensorProto.FLOAT, [None, 1])],
        [numpy_helper.from_array(weight, "weight"), numpy_helper.from_array(bias, "bias")],
    )
    model = helper.make_model(graph, producer_name="SnapShield AI", opset_imports=[helper.make_opsetid("", OPSET)])
    model.ir_version = min(model.ir_version, 10)
    metadata = json.loads((ARTIFACT_DIR / "model_metadata.json").read_text(encoding="utf-8"))
    model.metadata_props.add(key="model_name", value=metadata["model_name"])
    model.metadata_props.add(key="tokenization", value="External scikit-learn TfidfVectorizer artifact")
    output = ARTIFACT_DIR / "text_classifier.onnx"; onnx.checker.check_model(model); onnx.save(model, output)
    test_rows = (DATA_DIR / "test.tsv").read_text(encoding="utf-8").splitlines()[1:]
    texts = [row.split("\t", 1)[1] for row in test_rows]
    features = vectorizer.transform(texts).toarray().astype(np.float32)
    expected = classifier.predict_proba(vectorizer.transform(texts))[:, 1]
    session = ort.InferenceSession(str(output), providers=["CPUExecutionProvider"])
    actual = session.run(["probability"], {"features": features})[0][:, 0]
    difference = np.abs(expected - actual)
    qdq_output = ARTIFACT_DIR / "text_classifier.qdq.onnx"
    # ORT shape-inference currently mishandles some Unicode Windows paths. Quantize
    # in an ASCII-safe temporary directory, then copy the verified artifact back.
    with tempfile.TemporaryDirectory(prefix="snapshield_onnx_") as temporary:
        temp_input = Path(temporary) / "classifier.onnx"
        temp_output = Path(temporary) / "classifier.qdq.onnx"
        shutil.copy2(output, temp_input)
        calibration_rows = (DATA_DIR / "validation.tsv").read_text(encoding="utf-8").splitlines()[1:301]
        calibration_texts = [row.split("\t", 1)[1] for row in calibration_rows]
        calibration_features = vectorizer.transform(calibration_texts).toarray().astype(np.float32)
        quantize_static(str(temp_input), str(temp_output), FeatureCalibrationReader(calibration_features), quant_format=QuantFormat.QDQ, activation_type=QuantType.QUInt8, weight_type=QuantType.QInt8, per_channel=False, op_types_to_quantize=["MatMul"])
        shutil.copy2(temp_output, qdq_output)
    onnx.checker.check_model(onnx.load(qdq_output))
    qdq_session = ort.InferenceSession(str(qdq_output), providers=["CPUExecutionProvider"])
    qdq_actual = qdq_session.run(["probability"], {"features": features})[0][:, 0]
    qdq_difference = np.abs(actual - qdq_actual)
    report = {"verified": True, "opset": OPSET, "ir_version": model.ir_version, "input": {"name": "features", "dtype": "float32", "shape": ["batch", feature_count]}, "output": {"name": "probability", "dtype": "float32", "shape": ["batch", 1]}, "operators": ["MatMul", "Add", "Sigmoid"], "samples_compared": len(texts), "comparison_set": "complete untouched held-out test split", "max_absolute_difference": float(difference.max()), "mean_absolute_difference": float(difference.mean()), "class_agreement_at_0_5": float(np.mean((expected >= .5) == (actual >= .5))), "onnx_size_bytes": output.stat().st_size, "runtime": ort.__version__, "provider": session.get_providers()[0], "qdq": {"path": qdq_output.name, "size_bytes": qdq_output.stat().st_size, "format": "QDQ", "activation_type": "QUInt8", "weight_type": "QInt8", "calibration_split": "first 300 validation records; no test records", "max_absolute_difference_vs_fp32": float(qdq_difference.max()), "mean_absolute_difference_vs_fp32": float(qdq_difference.mean()), "class_agreement_at_0_5": float(np.mean((actual >= .5) == (qdq_actual >= .5)))}, "qnn_note": "QDQ deployment candidate uses QuantizeLinear/DequantizeLinear around MatMul. Full HTP assignment must be verified with CPU fallback disabled on target hardware."}
    (ARTIFACT_DIR / "onnx_validation.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2)); return output


if __name__ == "__main__":
    export()
