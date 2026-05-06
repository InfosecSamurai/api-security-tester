from __future__ import annotations

import json
import os
from datetime import datetime
from pathlib import Path
from typing import Any


def _write_json_report(scan_results: dict[str, Any], output_dir: Path, timestamp: str) -> Path:
    report_path = output_dir / f"api_scan_report_{timestamp}.json"
    with report_path.open("w", encoding="utf-8") as report_file:
        json.dump(scan_results, report_file, indent=4)
    return report_path


def _write_markdown_report(scan_results: dict[str, Any], output_dir: Path, timestamp: str) -> Path:
    report_path = output_dir / f"api_scan_report_{timestamp}.md"
    summary = scan_results.get("summary", {})
    lines = [
        "# API Security Tester Report",
        "",
        f"**Target:** `{scan_results.get('target', 'unknown')}`",
        f"**Timestamp:** `{scan_results.get('timestamp', 'unknown')}`",
        f"**Checks Run:** {summary.get('checks_run', 0)}",
        f"**Findings:** {summary.get('findings', 0)}",
        f"**Errors:** {summary.get('errors', 0)}",
        f"**Duration:** {summary.get('duration_seconds', 0)} seconds",
        "",
        "## Findings",
        "",
    ]

    for vulnerability in scan_results.get("vulnerabilities", []):
        status = "Finding" if vulnerability.get("finding") else "No Finding"
        lines.extend([
            f"### {vulnerability.get('name', 'Unnamed Check')}",
            "",
            f"- **Severity:** {vulnerability.get('severity', 'Unknown')}",
            f"- **Status:** {status}",
            f"- **Description:** {vulnerability.get('description', '')}",
            "",
            "```json",
            json.dumps(vulnerability.get("results", []), indent=2),
            "```",
            "",
        ])

    with report_path.open("w", encoding="utf-8") as report_file:
        report_file.write("\n".join(lines))
    return report_path


def generate_report(scan_results: dict[str, Any], output_dir: str = "reports") -> dict[str, str]:
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    json_report = _write_json_report(scan_results, output_path, timestamp)
    markdown_report = _write_markdown_report(scan_results, output_path, timestamp)

    return {
        "json": os.fspath(json_report),
        "markdown": os.fspath(markdown_report),
    }
