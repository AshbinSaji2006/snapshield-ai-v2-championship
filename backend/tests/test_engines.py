from backend.app.pii_analyzer import analyze_pii
from backend.app.orchestrator import analyze_text_full, analyze_url_full


def test_phishing_message_is_high_risk():
    result = analyze_text_full("URGENT: Your bank account is suspended. Verify your password and OTP at http://paypa1-secure.example/login immediately.", False)
    assert result["risk_score"] >= 50
    assert result["severity"] in {"high", "critical"}
    assert len(result["signals"]) >= 3


def test_normal_message_not_high_risk():
    result = analyze_text_full("Can we move our project meeting to Tuesday afternoon?", False)
    assert result["risk_score"] < 25


def test_url_never_networks_and_finds_ip():
    result = analyze_url_full("http://192.0.2.1:8080/verify/login.exe", False)
    ids = {item["id"] for item in result["signals"]}
    assert {"URL_IP_HOST", "URL_PORT", "URL_FILE_TYPE"} <= ids


def test_pii_redaction_and_luhn():
    findings, redacted = analyze_pii("Email alex@example.com card 4111 1111 1111 1111")
    assert {item["type"] for item in findings} >= {"email", "payment_card"}
    assert "alex@example.com" not in redacted
    assert "4111 1111 1111 1111" not in redacted

