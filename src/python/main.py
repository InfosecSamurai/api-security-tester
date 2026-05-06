#!/usr/bin/env python3
from __future__ import annotations

import argparse
import sys

from core.config_loader import load_config
from core.scanner import APIScanner
from core.utils import normalize_base_url
from core.reporter import generate_report


def main() -> int:
    parser = argparse.ArgumentParser(description="API Security Tester")
    parser.add_argument("--target", required=True, help="Target API base URL, for example https://example.com/api")
    parser.add_argument("--config", default=None, help="Optional YAML configuration file path")
    parser.add_argument("--output", default="reports", help="Output directory for reports")
    args = parser.parse_args()

    try:
        target = normalize_base_url(args.target)
        config = load_config(args.config)
    except Exception as exc:
        print(f"Configuration error: {exc}", file=sys.stderr)
        return 2

    print(f"Starting security scan for {target}")
    scanner = APIScanner(target_url=target, config=config)
    scan_results = scanner.run_scan()

    print("Generating reports...")
    report_paths = generate_report(scan_results, output_dir=args.output)
    print(f"JSON report: {report_paths['json']}")
    print(f"Markdown report: {report_paths['markdown']}")
    print(
        "Summary: "
        f"{scan_results['summary']['checks_run']} checks, "
        f"{scan_results['summary']['findings']} findings, "
        f"{scan_results['summary']['errors']} errors"
    )
    return 1 if scan_results["summary"].get("findings", 0) else 0


if __name__ == "__main__":
    raise SystemExit(main())
