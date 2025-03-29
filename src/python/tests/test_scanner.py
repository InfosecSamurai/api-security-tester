import pytest
from unittest.mock import patch
from core.scanner import APIScanner
from vulnerabilities.sql_injection import check as sql_check

@pytest.fixture
def mock_config():
    return {
        "sql_injection": {
            "test_payloads": ["test_payload"]
        }
    }

@patch('core.scanner.sql_injection.check')
def test_scanner_run_scan(mock_check, mock_config):
    mock_check.return_value = {"name": "SQL Injection", "results": []}
    scanner = APIScanner("http://test.com", mock_config)
    results = scanner.run_scan()
    assert "vulnerabilities" in results
    assert len(results["vulnerabilities"]) > 0
    mock_check.assert_called_once()
