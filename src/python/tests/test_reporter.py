import os
import pytest
from core.reporter import generate_report

@pytest.fixture
def sample_results():
    return {
        "target": "http://test.com",
        "vulnerabilities": []
    }

def test_generate_report(sample_results, tmp_path):
    report_path = generate_report(sample_results, str(tmp_path))
    assert os.path.exists(report_path)
    with open(report_path, 'r') as f:
        content = f.read()
        assert "http://test.com" in content
