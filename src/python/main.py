#!/usr/bin/env python3
import argparse
from core.scanner import APIScanner
from core.reporter import generate_report
from core.config_loader import load_config

def main():
    parser = argparse.ArgumentParser(description="API Security Tester")
    parser.add_argument("--target", required=True, help="Target API URL")
    parser.add_argument("--config", default="config/config.yaml", help="Configuration file path")
    parser.add_argument("--output", default="reports", help="Output directory for reports")
    args = parser.parse_args()

    config = load_config(args.config)
    scanner = APIScanner(target_url=args.target, config=config)
    
    print(f"Starting security scan for {args.target}")
    scan_results = scanner.run_scan()
    
    print("Generating report...")
    report_path = generate_report(scan_results, output_dir=args.output)
    print(f"Report generated at: {report_path}")

if __name__ == "__main__":
    main()
