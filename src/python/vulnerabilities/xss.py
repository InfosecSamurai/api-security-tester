from __future__ import annotations

from typing import Any

from core.utils import build_url, get_request_options, make_api_request


def check(target_url: str, config: dict[str, Any]) -> dict[str, Any]:
    xss_config = config.get("xss", {})
    test_payloads = xss_config.get("test_payloads", [])
    parameter = xss_config.get("parameter", "input")
    endpoint = xss_config.get("test_endpoint", "")
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
        vulnerable = payload in content
        results.append({
            "payload": payload,
            "url": response.get("url"),
            "status_code": response.get("status_code"),
            "elapsed_ms": response.get("elapsed_ms"),
            "reflected": vulnerable,
            "vulnerable": vulnerable,
        })

    return {
        "name": "Cross-Site Scripting (XSS)",
        "description": "Tests whether supplied payloads are reflected unsanitized in API responses.",
        "severity": "Medium",
        "finding": any(result.get("vulnerable") for result in results),
        "results": results,
    }
