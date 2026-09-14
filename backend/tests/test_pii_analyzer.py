import pytest

from backend.app.pii_analyzer import analyze_pii


@pytest.mark.parametrize("text,kind,secret", [
    ("mail alex@example.com", "email", "alex@example.com"),
    ("call +1 (202) 555-0182", "phone", "+1 (202) 555-0182"),
    ("card 4111 1111 1111 1111", "payment_card", "4111 1111 1111 1111"),
    ("Bearer abcdefghijklmnopqrstuvwxyz", "bearer_token", "abcdefghijklmnopqrstuvwxyz"),
    ("api_key=abcdefghijklmnop123456", "api_key", "abcdefghijklmnop123456"),
    ("password=hunter2-example", "password", "hunter2-example"),
    ("-----BEGIN PRIVATE KEY-----", "private_key", "BEGIN PRIVATE KEY"),
])
def test_sensitive_value_is_detected_and_hidden(text, kind, secret):
    findings, redacted = analyze_pii(text)
    assert kind in {item["type"] for item in findings}
    assert secret not in redacted


def test_valid_jwt_is_detected():
    token = "eyJhbGciOiJIUzI1NiJ9.eyJzdWIiOiIxMjM0NTY3ODkwIn0.abcdefghijklmnopqrstuvwxyz"
    assert "jwt" in {item["type"] for item in analyze_pii(token)[0]}


def test_invalid_card_candidate_not_reported():
    assert "payment_card" not in {item["type"] for item in analyze_pii("1234 5678 9012 3456")[0]}


def test_spans_reference_original_text():
    text = "before alex@example.com after"
    finding = analyze_pii(text)[0][0]
    assert text[finding["start"]:finding["end"]] == "alex@example.com"

