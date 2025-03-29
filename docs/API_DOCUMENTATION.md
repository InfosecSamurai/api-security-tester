# API Security Tester - API Documentation

## Overview
The API Security Tester is a tool designed to identify common vulnerabilities in RESTful APIs. This document describes the internal API of the tool.

## Core Components

### Scanner
- `APIScanner(targetUrl, config)`: Creates a new scanner instance
- `runScan()`: Executes all vulnerability checks against the target URL

### Vulnerability Checks
Each vulnerability check follows the same pattern:
- Takes `targetUrl` and `config` as parameters
- Returns an object with:
  - `name`: Vulnerability name
  - `description`: Brief description
  - `severity`: High/Medium/Low
  - `results`: Array of test results

### Reporter
- `generateReport(scanResults, outputDir)`: Generates a JSON report file

## Adding New Vulnerability Checks
1. Create a new file in the `vulnerabilities` directory
2. Implement a `check(targetUrl, config)` function
3. Add the check to the `APIScanner.checks` array
