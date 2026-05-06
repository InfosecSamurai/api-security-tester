from __future__ import annotations

from typing import Any

from core.utils import build_url, get_request_options, make_api_request


def check(target_url: str, config: dict[str, Any]) -> dict[str, Any]:
    sql_config = config.get("sql_injection", {})
    test_payloads = sql_config.get("test_payloads", [])
    parameter = sql_config.get("parameter", "input")
    endpoint = sql_config.get("test_endpoint", "")
    error_signatures = [signature.lower() for signature in sql_config.get("error_signatures", [])]
    request_options = get_request_options(config)

    results = []
    for payload in test_payloads:
        response = make_api_request(
            build_url(target_url, endpoint),
            method="GET",
            params={parameter: payload},
            **request_options,
        )

        if "error" in response:
            results.append({"payload": payload, "error": response["error"], "vulnerable": False})
            continue

        content = response.get("content", "") or ""
        content_lower = content.lower()
        matched_signatures = [signature for signature in error_signatures if signature in content_lower]
        vulnerable = response.get("status_code", 0) >= 500 or bool(matched_signatures)
        results.append({
            "payload": payload,
            "url": response.get("url"),
            "status_code": response.get("status_code"),
            "elapsed_ms": response.get("elapsed_ms"),
            "matched_signatures": matched_signatures,
            "vulnerable": vulnerable,
        })

    return {
        "name": "SQL Injection",
        "description": "Tests query-parameter input for SQL error disclosure and unstable server responses.",
        "severity": "High",
        "finding": any(result.get("vulnerable") for result in results),
        "results": results,
    }
