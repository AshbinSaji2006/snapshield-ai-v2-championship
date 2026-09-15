import hashlib
import json

import pytest
from fastapi.testclient import TestClient

from backend.app.adaptive import route
from backend.app.brand_analyzer import analyze_brand_mismatch
from backend.app.deep_guard import DeepGuard, get_deep_guard
from backend.app.domain_intelligence import domain_facts
from backend.app.evidence_graph import build_graph, sanitized_export
from backend.app.live_shield import LiveShield
from backend.app.main import app
from backend.app.normalization import normalize_security, normalization_signals
from backend.app.orchestrator import analyze_text_full
from backend.app.url_analyzer import analyze_url


def test_normalizer_preserves_original_and_builds_separate_security_view():
    source = "Pay&#32;at hxxp://paypa\u043b[.]example/login\u200b now"
    evidence = normalize_security(source)
    assert evidence.original_text == source
    assert "http://" in evidence.normalized_security_text
    assert "\u200b" not in evidence.normalized_security_text
    assert len(evidence.transformations) >= 3
    assert normalization_signals(evidence)


@pytest.mark.parametrize("source,expected", [
    ("hxxps://example[.]com", "https://example.com"),
    ("https : // example.com", "https://example.com"),
    ("p.a.s.s.w.o.r.d", "password"),
])
def test_security_normalization_recovers_bounded_obfuscations(source, expected):
    assert expected in normalize_security(source).normalized_security_text


def test_domain_engine_uses_offline_public_suffix_rules():
    facts = domain_facts("login.accounts.example.co.uk")
    assert facts["registrable_domain"] == "example.co.uk"
    assert facts["psl_available"] is True
    assert facts["idna_valid"] is True


def test_domain_engine_handles_invalid_idna_without_crashing():
    facts = domain_facts("bad\ufffdhost.example")
    assert facts["idna_valid"] is False
    with pytest.raises(ValueError):
        analyze_url("https://bad\ufffdhost.example/login")


def test_url_engine_rejects_invalid_port_safely():
    with pytest.raises(ValueError, match="invalid port"):
        analyze_url("https://example.com:notaport/login")


def test_brand_engine_distinguishes_official_and_mismatched_domains():
    assert analyze_brand_mismatch("SBI notice https://sbi.co.in/security", ["https://sbi.co.in/security"]) == []
    mismatch = analyze_brand_mismatch("SBI notice https://sbi-update.example/login", ["https://sbi-update.example/login"])
    assert mismatch[0]["id"] == "BRAND_DOMAIN_MISMATCH"
    assert mismatch[0]["expected_domains"] == ["sbi.co.in", "onlinesbi.sbi"]


def test_router_keeps_extreme_safe_probability_on_fast_path():
    decision = route(.0001, [])
    assert decision["requested_deep"] is False
    assert decision["decision_class"] == "FAST_ONLY_SAFE"


def test_router_escalates_ambiguous_probability_with_reason():
    decision = route(.35, [])
    assert decision["requested_deep"] is True
    assert decision["decision_class"] == "ESCALATE_UNCERTAIN"
    assert decision["entropy_threshold"] == .045


def test_router_does_not_apply_english_neural_model_to_devanagari():
    decision = route(.4, [], script="Devanagari")
    assert decision["requested_deep"] is False
    assert decision["supported_neural_language"] is False


def test_deep_guard_artifact_is_hash_gated(tmp_path):
    (tmp_path / "model.onnx").write_bytes(b"not an onnx model")
    (tmp_path / "tokenizer.json").write_text("{}", encoding="utf-8")
    manifest = {"deployment_approved": True, "file_hashes": {"model.onnx": "wrong", "tokenizer.json": "wrong"}}
    (tmp_path / "manifest.json").write_text(json.dumps(manifest), encoding="utf-8")
    guard = DeepGuard(tmp_path)
    assert guard.ready is False
    assert "unavailable" in guard.reason.lower()


def test_selected_deep_guard_runs_exact_local_onnx():
    guard = get_deep_guard()
    assert guard.ready is True
    result = guard.predict("Urgent: verify your account password at hxxp://bank-update.example")
    assert result and result["provider"] == "CPUExecutionProvider"
    assert 0 <= result["probability"] <= 1


def test_evidence_graph_is_structured_and_redacts_node_labels():
    result = {"input_type": "text", "severity": "high", "risk_score": 80,
              "detected_urls": [], "signals": [{"id": "PII_PRESENT", "name": "Sensitive data", "description": "detected", "contribution": 3, "evidence": "priya@example.com"}],
              "details": {"routing": {"path": "fast", "reasons": ["test"]}}}
    graph = build_graph(result, [{"kind": "TextEvidence", "label": "Submitted text", "text": "priya@example.com"}])
    assert graph["nodes"] and graph["edges"]
    assert "priya@example.com" not in json.dumps(graph)
    assert any(node["type"] == "RiskDecision" for node in graph["nodes"])


def test_sanitized_export_excludes_source_and_hash_fields():
    exported = sanitized_export({"id": "1", "input_hash": "secret", "source": "raw", "severity": "high", "evidence": []})
    assert "input_hash" not in json.dumps(exported)
    assert "source" not in exported["incident"]


def test_live_shield_is_off_by_default_and_does_not_call_analyzer():
    calls = []
    shield = LiveShield(analyzer=lambda text, save: calls.append(text))
    assert shield.process("copied secret") is None
    assert calls == []


def test_live_shield_deduplicates_and_rate_limits_without_persistence():
    now = [10.0]
    def analyze(text, save):
        assert save is False
        return {"risk_score": 90, "severity": "critical", "signals": [], "details": {}}
    shield = LiveShield(analyzer=analyze, clock=lambda: now[0]); shield.start(start_thread=False)
    assert shield.process("first suspicious message") is not None
    assert shield.process("first suspicious message") is None
    assert shield.process("second suspicious message") is None
    now[0] += 3.1
    assert shield.process("second suspicious message") is not None
    assert shield.status()["persistence"] is False
    shield.stop()
    assert shield.latest() is None


def test_live_api_requires_explicit_consent():
    with TestClient(app) as client:
        response = client.post("/api/live/control", json={"enabled": True, "consent": False})
        assert response.status_code == 422
        assert client.get("/api/live/status").json()["enabled"] is False


def test_full_analysis_exposes_real_routing_and_graph_without_saving():
    result = analyze_text_full("SBI account blocked. Send OTP at hxxp://sbi-update[.]example/login", False)
    assert result["details"]["routing"]["deep_executed"] is True
    assert result["details"]["deep_guard"]["provider"] == "CPUExecutionProvider"
    assert result["details"]["evidence_graph"]["nodes"]
    assert result["id"] is None


def test_deployment_manifest_hashes_match_every_declared_artifact():
    root = get_deep_guard().manifest
    directory = __import__("pathlib").Path(__file__).resolve().parents[2] / "ml/v2/deep_guard"
    for name, expected in root["file_hashes"].items():
        assert hashlib.sha256((directory / name).read_bytes()).hexdigest() == expected


def test_normal_analysis_succeeds_with_network_connections_disabled(monkeypatch):
    import socket
    attempted = []
    def blocked(*args, **kwargs):
        attempted.append((args, kwargs)); raise AssertionError("network connection attempted")
    monkeypatch.setattr(socket, "create_connection", blocked)
    result = analyze_text_full("SBI account blocked. Send OTP at http://sbi-update.example", False)
    assert result["risk_score"] >= 50
    assert attempted == []


def test_xss_like_text_is_data_not_markup_or_code():
    payload = '<script>alert("snapshield")</script> verify password'
    result = analyze_text_full(payload, False)
    assert result["details"]["normalization"]["original_text_redacted"] == payload
    assert all("<script>" not in node["label"] for node in result["details"]["evidence_graph"]["nodes"])


def test_oversized_normalization_input_is_rejected_before_analysis():
    with pytest.raises(ValueError, match="50,000"):
        normalize_security("x" * 50_001)
