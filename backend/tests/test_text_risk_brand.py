import pytest

from backend.app.brand_analyzer import analyze_brand_mismatch
from backend.app.orchestrator import analyze_text_full
from backend.app.risk_engine import explain, fuse, recommendations, severity_for
from backend.app.text_analyzer import analyze_text


@pytest.mark.parametrize("text,signal", [
    ("URGENT: act now", "TXT_URGENCY"),
    ("Your account will be suspended", "TXT_ACCOUNT_THREAT"),
    ("Verify your password now", "TXT_CREDENTIAL"),
    ("Send the OTP", "TXT_OTP"),
    ("Pay using gift cards", "TXT_PAYMENT"),
    ("You won a lottery prize", "TXT_PRIZE"),
    ("Your parcel is held, pay the fee", "TXT_DELIVERY"),
    ("CEO says keep this confidential", "TXT_AUTHORITY"),
    ("Install AnyDesk for remote access", "TXT_REMOTE"),
])
def test_text_rules(text, signal):
    assert signal in {item["id"] for item in analyze_text(text)["signals"]}


def test_zero_width_obfuscation_is_recorded():
    assert "TXT_ZERO_WIDTH" in {item["id"] for item in analyze_text("pass\u200bword")["signals"]}


def test_mixed_script_is_recorded():
    assert "TXT_MIXED_SCRIPT" in {item["id"] for item in analyze_text("Micrоsoft")["signals"]}


def test_duplicate_urls_are_collapsed():
    result = analyze_text("https://example.com https://example.com")
    assert result["urls"] == ["https://example.com"]


def test_brand_mismatch_is_specific():
    signal = analyze_brand_mismatch("SBI account alert", ["https://unrelated.example/login"])[0]
    assert signal["brand"] == "SBI" and signal["observed_domain"] == "unrelated.example"


def test_official_brand_domain_does_not_mismatch():
    assert analyze_brand_mismatch("Microsoft account", ["https://account.microsoft.com/security"]) == []


def test_protective_advice_is_not_treated_as_request():
    ids = {item["id"] for item in analyze_text("SBI employees never ask you to share an OTP or password.")["signals"]}
    assert "TXT_SAFETY_ADVICE" in ids and "TXT_OTP" not in ids and "TXT_CREDENTIAL" not in ids


@pytest.mark.parametrize("score,expected", [(0,"low"),(24,"low"),(25,"moderate"),(50,"high"),(75,"critical"),(100,"critical")])
def test_severity_thresholds(score, expected):
    assert severity_for(score) == expected


def test_single_weak_signal_is_discounted():
    assert fuse([{"contribution": 10}]) == 8


def test_explanation_uses_real_description_and_evidence():
    message = explain(60, "test", [{"name":"Domain mismatch","description":"Observed host is unrelated.","contribution":24,"evidence":"evil.example"}])
    assert "Observed host is unrelated" in message and "evil.example" in message


def test_credentials_produce_actionable_recommendation():
    actions = recommendations(60, [{"id":"TXT_CREDENTIAL"}])
    assert any("password" in item for item in actions)


def test_full_brand_phish_is_high():
    result = analyze_text_full("SBI: verify your password at https://unrelated.example/login immediately", False)
    assert result["risk_score"] >= 50 and any(item["id"] == "BRAND_DOMAIN_MISMATCH" for item in result["signals"])

