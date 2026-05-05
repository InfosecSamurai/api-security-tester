from __future__ import annotations

from copy import deepcopy
from pathlib import Path
from typing import Any, Mapping

import yaml

DEFAULT_CONFIG: dict[str, Any] = {
    "general": {
        "timeout_seconds": 10,
        "verify_ssl": True,
        "allow_redirects": True,
        "user_agent": "api-security-tester/1.0",
        "headers": {},
    },
    "tests": {
        "sql_injection": True,
        "xss": True,
        "broken_auth": True,
        "sensitive_data": True,
        "rate_limiting": True,
    },
    "sql_injection": {
        "test_endpoint": "",
        "parameter": "input",
        "test_payloads": [
            "'",
            "\"",
            "' OR '1'='1",
            "' OR 1=1--",
        ],
        "error_signatures": [
            "sql syntax",
            "mysql",
            "postgresql",
            "sqlite",
            "odbc",
            "ora-",
            "syntax error",
            "unterminated quoted string",
        ],
    },
    "xss": {
        "test_endpoint": "",
        "parameter": "input",
        "test_payloads": [
            "<script>alert('xss')</script>",
            "\"><svg/onload=alert('xss')>",
        ],
    },
    "broken_auth": {
        "auth_endpoints": {
            "login": "/login",
            "protected": "/admin",
        },
        "test_credentials": [
            {"username": "admin", "password": "admin"},
            {"username": "user", "password": "password"},
        ],
        "success_indicators": ["token", "access_token", "jwt", "session"],
    },
    "sensitive_data": {
        "endpoints": ["/users", "/profile", "/account"],
        "patterns": {
            "password": "password",
            "api_key": "api[_-]?key",
            "secret": "secret",
            "token": "access[_-]?token|refresh[_-]?token|bearer",
            "ssn": "\\b\\d{3}-\\d{2}-\\d{4}\\b",
            "credit_card": "\\b(?:\\d[ -]*?){13,16}\\b",
        },
    },
    "rate_limiting": {
        "test_endpoint": "/api/data",
        "max_requests": 20,
        "threshold_seconds": 10,
        "delay_seconds": 0.05,
    },
}


def _deep_merge(base: dict[str, Any], override: Mapping[str, Any]) -> dict[str, Any]:
    merged = deepcopy(base)
    for key, value in override.items():
        if isinstance(value, Mapping) and isinstance(merged.get(key), dict):
            merged[key] = _deep_merge(merged[key], value)
        else:
            merged[key] = value
    return merged


def _resolve_config_path(config_path: str | None) -> Path | None:
    if not config_path:
        default_path = Path(__file__).resolve().parents[1] / "config" / "config.yaml"
        return default_path if default_path.exists() else None

    candidate = Path(config_path).expanduser()
    if candidate.exists():
        return candidate

    script_relative = Path(__file__).resolve().parents[1] / config_path
    if script_relative.exists():
        return script_relative

    raise FileNotFoundError(f"Config file not found: {config_path}")


def load_config(config_path: str | None = None) -> dict[str, Any]:
    resolved_path = _resolve_config_path(config_path)
    if resolved_path is None:
        return deepcopy(DEFAULT_CONFIG)

    with resolved_path.open("r", encoding="utf-8") as config_file:
        loaded = yaml.safe_load(config_file) or {}

    if not isinstance(loaded, Mapping):
        raise ValueError("Config file must contain a YAML mapping/object at the top level")

    return _deep_merge(DEFAULT_CONFIG, loaded)
