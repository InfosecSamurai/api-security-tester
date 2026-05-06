from __future__ import annotations

from typing import Any

from core.utils import build_url, get_request_options, make_api_request, redact_value


def _content_contains_success_indicator(content: str, indicators: list[str]) -> bool:
    lowered = content.lower()
    return any(indicator.lower() in lowered for indicator in indicators)


def check(target_url: str, config: dict[str, Any]) -> dict[str, Any]:
    auth_config = config.get("broken_auth", {})
    auth_endpoints = auth_config.get("auth_endpoints", {"login": "/login", "protected": "/admin"})
    weak_creds = auth_config.get("test_credentials", [])
    success_indicators = auth_config.get("success_indicators", ["token", "session"])
    request_options = get_request_options(config)

    results = []
    for creds in weak_creds:
        response = make_api_request(
            build_url(target_url, auth_endpoints.get("login", "/login")),
            method="POST",
            json_data=creds,
            **request_options,
        )

        if "error" in response:
            results.append({
                "test": "weak_credentials",
                "credentials": redact_value(creds),
                "error": response["error"],
                "vulnerable": False,
            })
            continue

        content = response.get("content", "") or ""
        vulnerable = response.get("status_code") in {200, 201} and _content_contains_success_indicator(content, success_indicators)
        results.append({
            "test": "weak_credentials",
            "credentials": redact_value(creds),
            "status_code": response.get("status_code"),
            "elapsed_ms": response.get("elapsed_ms"),
            "vulnerable": vulnerable,
        })

    protected_endpoint = auth_endpoints.get("protected")
    if protected_endpoint:
        response = make_api_request(
            build_url(target_url, protected_endpoint),
            method="GET",
            **request_options,
        )
        results.append({
            "test": "unauthenticated_protected_endpoint_access",
            "endpoint": protected_endpoint,
            "status_code": response.get("status_code"),
            "accessible_without_auth": response.get("status_code") in {200, 201, 202},
            "vulnerable": response.get("status_code") in {200, 201, 202},
            "error": response.get("error"),
        })

    return {
        "name": "Broken Authentication",
        "description": "Tests weak default credentials and unauthenticated access to configured protected endpoints.",
        "severity": "High",
        "finding": any(result.get("vulnerable") for result in results),
        "results": results,
    }
