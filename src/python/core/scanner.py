from __future__ import annotations

import time
from typing import Any, Callable

from vulnerabilities import broken_auth, rate_limiting, sensitive_data, sql_injection, xss


class APIScanner:
    def __init__(self, target_url: str, config: dict[str, Any]):
        self.target_url = target_url.rstrip("/")
        self.config = config
        self.vulnerability_checks: list[tuple[str, Callable[[str, dict[str, Any]], dict[str, Any]]]] = [
            ("sql_injection", sql_injection.check),
            ("xss", xss.check),
            ("broken_auth", broken_auth.check),
            ("sensitive_data", sensitive_data.check),
            ("rate_limiting", rate_limiting.check),
        ]

    def run_scan(self) -> dict[str, Any]:
        started = time.time()
        results: dict[str, Any] = {
            "target": self.target_url,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "vulnerabilities": [],
            "summary": {
                "checks_run": 0,
                "findings": 0,
                "errors": 0,
            },
        }

        enabled_tests = self.config.get("tests", {})
        for check_name, check in self.vulnerability_checks:
            if enabled_tests.get(check_name, True) is False:
                continue

            try:
                result = check(self.target_url, self.config)
                results["vulnerabilities"].append(result)
                results["summary"]["checks_run"] += 1
                if result.get("finding") is True:
                    results["summary"]["findings"] += 1
            except Exception as exc:  # keep full scan running even if one module fails
                results["summary"]["errors"] += 1
                results["vulnerabilities"].append({
                    "name": check_name,
                    "severity": "Unknown",
                    "finding": False,
                    "error": str(exc),
                    "results": [],
                })

        results["summary"]["duration_seconds"] = round(time.time() - started, 2)
        return results
