"""Deployment-focused checks that do not need a live cloud account."""

import json
import os
import re
from pathlib import Path
from unittest.mock import mock_open, patch

import config


ROOT = Path(__file__).resolve().parents[1]


def test_vercel_function_configuration_targets_the_flask_entrypoint():
    with (ROOT / "vercel.json").open(encoding="utf-8") as source:
        deployment = json.load(source)

    assert "app.py" in deployment["functions"]
    assert "tests/**" in deployment["functions"]["app.py"]["excludeFiles"]


def test_secret_key_falls_back_to_memory_when_the_filesystem_is_read_only():
    with (
        patch.dict(os.environ, {"SECRET_KEY": ""}, clear=False),
        patch("config.os.path.exists", return_value=False),
        patch("config.os.makedirs"),
        patch("builtins.open", mock_open()) as file_open,
    ):
        file_open.side_effect = OSError("read-only filesystem")
        generated = config._get_secret_key()

    assert re.fullmatch(r"[0-9a-f]{64}", generated)


def test_render_postgres_url_uses_the_installed_psycopg_driver():
    with patch.dict(os.environ, {"DATABASE_URL": "postgresql://user:pass@db:5432/bazi"}, clear=False):
        assert config._get_database_url() == "postgresql+psycopg://user:pass@db:5432/bazi"


def test_render_blueprint_declares_postgres_and_production_start_command():
    content = (ROOT / "render.yaml").read_text(encoding="utf-8")

    assert "runtime: python" in content
    assert "gunicorn --workers" in content
    assert "fromDatabase:" in content
    assert "name: bazi-oracle-db" in content
