from pathlib import Path

from backend.app import database
from backend.app.model_runtime import SklearnTextClassifier, _validated_qnn_candidate, get_classifier, model_status
from backend.app.model_runtime import runtime_manager as model_runtime_manager
from backend.app.runtime import RuntimeManager


def sample_result():
    return {"input_type":"text","risk_score":42,"severity":"moderate","threat_category":"test","classification":"suspicious","signals":[{"id":"X","name":"safe name","severity":"moderate"}],"processing_time_ms":1.2,"runtime":{"selected_provider":"CPUExecutionProvider"}}


def test_database_lifecycle_uses_sanitized_metadata(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATA_DIR", tmp_path); monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    database.init_db(); incident_id = database.create_incident(sample_result(), "a" * 64)
    item = database.get_incident(incident_id)
    assert item and item["classification"] == "suspicious" and item["evidence"][0]["id"] == "X"
    assert database.stats()["total_scans"] == 1
    assert database.delete_incident(incident_id) is True
    assert database.get_incident(incident_id) is None


def test_clear_incidents_returns_count(tmp_path, monkeypatch):
    monkeypatch.setattr(database, "DATA_DIR", tmp_path); monkeypatch.setattr(database, "DB_PATH", tmp_path / "test.db")
    database.init_db(); database.create_incident(sample_result(), "b" * 64); database.create_incident(sample_result(), "c" * 64)
    assert database.clear_incidents() == 2 and database.stats()["total_scans"] == 0


def test_runtime_does_not_equate_provider_presence_with_verification(tmp_path, monkeypatch):
    manager = RuntimeManager(); manager.onnx_providers = ["QNNExecutionProvider", "CPUExecutionProvider"]
    monkeypatch.setattr(manager, "snapdragon_validation", lambda: {"verified": False})
    assert manager.metadata()["snapdragon_npu_verified"] is False


def test_primary_model_is_onnx():
    assert model_status()["onnx"] is True
    assert get_classifier().predict("free prize now").provider == "CPUExecutionProvider"


def test_sklearn_fallback_agrees_with_onnx_class():
    text = "Claim your free reward now"
    primary = get_classifier().predict(text).probability
    fallback = SklearnTextClassifier().predict(text).probability
    assert abs(primary - fallback) < 1e-6


def test_qnn_candidate_requires_verified_report(tmp_path, monkeypatch):
    candidate = tmp_path / "candidate.onnx"; candidate.write_bytes(b"model")
    monkeypatch.setattr(model_runtime_manager, "snapdragon_validation", lambda: {"verified": False})
    assert _validated_qnn_candidate(["QNNExecutionProvider"], candidate) is False


def test_qnn_candidate_rejects_stale_hash(tmp_path, monkeypatch):
    candidate = tmp_path / "candidate.onnx"; candidate.write_bytes(b"model")
    report = {"verified": True, "execution_provider": "QNNExecutionProvider", "model": candidate.name, "model_sha256": "stale"}
    monkeypatch.setattr(model_runtime_manager, "snapdragon_validation", lambda: report)
    assert _validated_qnn_candidate(["QNNExecutionProvider"], candidate) is False


def test_qnn_candidate_accepts_exact_validated_artifact(tmp_path, monkeypatch):
    import hashlib
    candidate = tmp_path / "candidate.onnx"; candidate.write_bytes(b"model")
    report = {"verified": True, "execution_provider": "QNNExecutionProvider", "model": candidate.name, "model_sha256": hashlib.sha256(candidate.read_bytes()).hexdigest()}
    monkeypatch.setattr(model_runtime_manager, "snapdragon_validation", lambda: report)
    assert _validated_qnn_candidate(["QNNExecutionProvider"], candidate) is True
