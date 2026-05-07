import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from core.config_loader import load_config


def test_load_config_uses_defaults_when_no_path_is_given():
    config = load_config(None)

    assert config["general"]["timeout_seconds"] == 10
    assert config["tests"]["sql_injection"] is True
    assert config["sql_injection"]["parameter"] == "input"


def test_load_config_deep_merges_user_config(tmp_path):
    custom_config = tmp_path / "config.yaml"
    custom_config.write_text(
        "general:\n  timeout_seconds: 3\n"
        "rate_limiting:\n  max_requests: 2\n",
        encoding="utf-8",
    )

    config = load_config(str(custom_config))

    assert config["general"]["timeout_seconds"] == 3
    assert config["general"]["verify_ssl"] is True
    assert config["rate_limiting"]["max_requests"] == 2
    assert config["rate_limiting"]["threshold_seconds"] == 10
