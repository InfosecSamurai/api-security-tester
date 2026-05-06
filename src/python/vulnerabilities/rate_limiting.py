from __future__ import annotations

import time
from typing import Any

from core.utils import build_url, get_request_options, make_api_request


def check(target_url: str, config: dict[str, Any]) -> dict[str, Any]:
    rate_config = config.get("rate_limiting", {})
    endpoint = rate_config.get("test_endpoint", "/api/data")
    max_requests = int(rate_config.get("max_requests", 20))
    threshold = float(rate_config.get("threshold_seconds", 10))
    delay = float(rate_config.get("delay_seconds", 0.05))
    request_options = get_request_options(config)

    start_time = time.time()
    request_count = 0
    status_codes: list[int | None] = []
    rate_limit_hit = False
    last_response: dict[str, Any] = {}

    while time.time() - start_time < threshold and request_count < max_requests:
        last_response = make_api_request(
            build_url(target_url, endpoint),
            method="GET",
            **request_options,
        )
        request_count += 1
        status_codes.append(last_response.get("status_code"))

        if last_response.get("status_code") == 429:
            rate_limit_hit = True
            break
        if delay > 0:
            time.sleep(delay)

    elapsed = max(time.time() - start_time, 0.001)
    vulnerable = not rate_limit_hit and request_count >= max_requests
    results = [{
        "endpoint": endpoint,
        "requests_sent": request_count,
        "time_elapsed": round(elapsed, 2),
        "rate_limit_hit": rate_limit_hit,
        "requests_per_second": round(request_count / elapsed, 2),
        "last_status_code": last_response.get("status_code"),
        "status_codes_seen": sorted({code for code in status_codes if code is not None}),
        "vulnerable": vulnerable,
    }]

    return {
        "name": "Rate Limiting",
        "description": "Sends a bounded request burst and flags targets that never respond with HTTP 429.",
        "severity": "Medium",
        "finding": vulnerable,
        "results": results,
    }
