from __future__ import annotations

from copy import deepcopy
from typing import Any
from urllib.parse import urljoin, urlparse

import requests


class RequestBlockedError(ValueError):
    """Raised when a target URL is not allowed by scanner safety rules."""


def normalize_base_url(url: str) -> str:
    parsed = urlparse(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise ValueError("Target must be a valid http:// or https:// URL")
    return url.rstrip("/")


def build_url(base_url: str, endpoint: str = "") -> str:
    base = normalize_base_url(base_url)
    if not endpoint:
        return base
    return urljoin(f"{base}/", endpoint.lstrip("/"))


def redact_value(value: Any) -> Any:
    if isinstance(value, dict):
        redacted = {}
        for key, inner in value.items():
            lowered = str(key).lower()
            if any(marker in lowered for marker in ("password", "secret", "token", "key", "authorization")):
                redacted[key] = "[REDACTED]"
            else:
                redacted[key] = redact_value(inner)
        return redacted
    if isinstance(value, list):
        return [redact_value(item) for item in value]
    return value


def make_api_request(
    url: str,
    method: str = "GET",
    headers: dict[str, str] | None = None,
    params: dict[str, Any] | None = None,
    data: Any = None,
    json_data: Any = None,
    timeout: float = 10,
    verify_ssl: bool = True,
    allow_redirects: bool = True,
) -> dict[str, Any]:
    try:
        response = requests.request(
            method=method.upper(),
            url=url,
            headers=headers or {},
            params=params or {},
            data=data,
            json=json_data,
            timeout=timeout,
            verify=verify_ssl,
            allow_redirects=allow_redirects,
        )
        return {
            "status_code": response.status_code,
            "headers": dict(response.headers),
            "content": response.text,
            "url": response.url,
            "elapsed_ms": round(response.elapsed.total_seconds() * 1000, 2),
        }
    except requests.RequestException as exc:
        return {"error": str(exc), "url": url}


def get_request_options(config: dict[str, Any]) -> dict[str, Any]:
    general = deepcopy(config.get("general", {}))
    headers = general.get("headers") or {}
    user_agent = general.get("user_agent")
    if user_agent:
        headers.setdefault("User-Agent", user_agent)

    return {
        "headers": headers,
        "timeout": float(general.get("timeout_seconds", 10)),
        "verify_ssl": bool(general.get("verify_ssl", True)),
        "allow_redirects": bool(general.get("allow_redirects", True)),
    }
