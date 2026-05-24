"""Tests for pretest.config."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from pretest.config import PretestConfig, load_config


def test_default_config():
    cfg = load_config()
    assert isinstance(cfg, PretestConfig)
    assert cfg.test_dirs == ["tests"]
    assert cfg.planfiles_dir == ".planfiles"
    assert 0 < cfg.min_duplicate_score <= 1.0


def test_load_config_from_file(tmp_path: Path):
    cfg_file = tmp_path / ".pretest.yml"
    cfg_file.write_text(
        textwrap.dedent("""\
            packages:
              - myapp
            min_duplicate_score: 0.75
            planfiles_dir: tickets
        """)
    )
    cfg = load_config(cfg_file)
    assert cfg.packages == ["myapp"]
    assert cfg.min_duplicate_score == 0.75
    assert cfg.planfiles_dir == "tickets"


def test_load_config_missing_file():
    with pytest.raises(FileNotFoundError):
        load_config("/nonexistent/path/.pretest.yml")
