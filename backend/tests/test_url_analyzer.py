import pytest

from backend.app.url_analyzer import analyze_url, normalize_url


@pytest.mark.parametrize("url,signal", [
    ("http://example.com", "URL_INSECURE_SCHEME"),
    ("https://192.0.2.1/login", "URL_IP_HOST"),
    ("https://xn--pple-43d.example", "URL_PUNYCODE"),
    ("https://trusted.example@192.0.2.1/login", "URL_AT_SYMBOL"),
    ("https://example.com//verify", "URL_DOUBLE_SLASH"),
    ("https://a.b.c.d.e.example.com", "URL_SUBDOMAINS"),
    ("https://bit.ly/abc", "URL_SHORTENER"),
    ("https://example.com:8443/login", "URL_PORT"),
    ("https://example.com/%76erify", "URL_ENCODING"),
    ("https://example.com/payload.exe", "URL_FILE_TYPE"),
    ("https://paypa1-secure.example/login", "URL_BRAND_MISMATCH"),
    ("https://unrelated.example/paypal/login", "URL_BRAND_IN_PATH"),
])
def test_structural_signals(url, signal):
    assert signal in {item["id"] for item in analyze_url(url)["signals"]}


def test_safe_url_has_zero_score():
    assert analyze_url("https://example.com/docs")["score"] == 0


def test_defanged_url_is_normalized_without_networking():
    assert normalize_url("hxxp://example[.]com/login") == "http://example.com/login"


@pytest.mark.parametrize("url", ["file:///etc/passwd", "javascript:alert(1)", "not a host"])
def test_invalid_or_non_web_url_rejected(url):
    with pytest.raises(ValueError):
        analyze_url(url)

