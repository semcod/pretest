"""Configuration management for testless."""

from __future__ import annotations

from pathlib import Path

import yaml
from pydantic import BaseModel, Field


class TestlessConfig(BaseModel):
    """Top-level configuration for testless."""

    # Source package(s) to measure coverage for
    packages: list[str] = Field(default_factory=list)

    # Directories that contain tests
    test_dirs: list[str] = Field(default=["tests"])

    # Minimum duplicate score to flag as a duplicate (0–1)
    min_duplicate_score: float = 0.85

    # Minimum line overlap fraction to consider two tests redundant (0–1)
    min_coverage_overlap: float = 0.85

    # Output directory for planfiles
    planfiles_dir: str = ".planfiles"

    # Output directory for coverage data
    coverage_dir: str = ".coverage_data"

    # pytest extra arguments passed verbatim to subprocess
    pytest_args: list[str] = Field(default_factory=list)


_DEFAULT_CONFIG_FILES = [".testless.yml", ".testless.yaml", "testless.yml", "testless.yaml"]


def load_config(path: str | Path | None = None) -> TestlessConfig:
    """Load config from a YAML file, falling back to defaults."""
    if path is not None:
        cfg_path = Path(path)
        if not cfg_path.exists():
            raise FileNotFoundError(f"Config file not found: {cfg_path}")
        with cfg_path.open() as fh:
            data = yaml.safe_load(fh) or {}
        return TestlessConfig(**data)

    for name in _DEFAULT_CONFIG_FILES:
        candidate = Path(name)
        if candidate.exists():
            with candidate.open() as fh:
                data = yaml.safe_load(fh) or {}
            return TestlessConfig(**data)

    return TestlessConfig()
