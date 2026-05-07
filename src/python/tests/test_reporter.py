import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.reporter import generate_report


def test_generate_report_writes_json_and_markdown(tmp_path):
    scan_results = {
        "target": "https://example.com/api",
        "timestamp": "2026-01-01T00:00:00Z",
        "summary": {"checks_run": 1, "findings": 0, "errors": 0, "duration_seconds": 0.1},
        "vulnerabilities": [
            {
                "name": "Example",
                "severity": "Low",
                "finding": False,
                "description": "Example check",
                "results": [],
            }
        ],
    }

    paths = generate_report(scan_results, str(tmp_path))

    json_path = Path(paths["json"])
    markdown_path = Path(paths["markdown"])
    assert json_path.exists()
    assert markdown_path.exists()
    assert json.loads(json_path.read_text(encoding="utf-8"))["target"] == "https://example.com/api"
    assert "API Security Tester Report" in markdown_path.read_text(encoding="utf-8")
