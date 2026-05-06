from __future__ import annotations

import re
from typing import Any

from core.utils import build_url, get_request_options, make_api_request


def check(target_url: str, config: dict[str, Any]) -> dict[str, Any]:
    data_config = config.get("sensitive_data", {})
    endpoints_to_check = data_config.get("endpoints", [])
    patterns = data_config.get("patterns", {})
    compiled_patterns = {
        name: re.compile(pattern, re.IGNORECASE)
        for name, pattern in patterns.items()
    }
    request_options = get_request_options(config)

    results = []
    for endpoint in endpoints_to_check:
        response = make_api_request(
            build_url(target_url, endpoint),
            method="GET",
            **request_options,
        )

        if "error" in response:
            results.append({"endpoint": endpoint, "error": response["error"], "vulnerable": False})
            continue

        content = response.get("content", "") or ""
        fields_found = [name for name, pattern in compiled_patterns.items() if pattern.search(content)]
        exposed = response.get("status_code") in {200, 201, 202} and bool(fields_found)
        results.append({
            "endpoint": endpoint,
            "status_code": response.get("status_code"),
            "elapsed_ms": response.get("elapsed_ms"),
            "sensitive_data_exposed": exposed,
            "fields_found": fields_found,
            "vulnerable": exposed,
        })

    return {
        "name": "Sensitive Data Exposure",
        "description": "Checks configured endpoints for common sensitive fields and secrets in unauthenticated responses.",
        "severity": "High",
        "finding": any(result.get("vulnerable") for result in results),
        "results": results,
    }
