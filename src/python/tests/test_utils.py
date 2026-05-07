import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.utils import build_url, normalize_base_url, redact_value


def test_normalize_base_url_rejects_non_http_urls():
    with pytest.raises(ValueError):
        normalize_base_url("ftp://example.com")


def test_build_url_joins_base_and_endpoint():
    assert build_url("https://example.com/api", "/users") == "https://example.com/api/users"


def test_redact_value_masks_sensitive_keys():
    data = {
        "username": "admin",
        "password": "admin",
        "nested": {"access_token": "abc123"},
    }

    redacted = redact_value(data)

    assert redacted["username"] == "admin"
    assert redacted["password"] == "[REDACTED]"
    assert redacted["nested"]["access_token"] == "[REDACTED]"
