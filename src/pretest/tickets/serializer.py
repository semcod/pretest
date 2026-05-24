"""Serialize Planfile objects to YAML files."""

from __future__ import annotations

import json
from pathlib import Path

from pretest.models.planfile import Planfile


def write_planfiles(planfiles: list[Planfile], output_dir: str | Path) -> list[Path]:
    """Write each Planfile to a YAML file in *output_dir*. Returns list of paths."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []

    for pf in planfiles:
        filename = f"{pf.id}.yml"
        path = out / filename
        path.write_text(pf.to_yaml(), encoding="utf-8")
        written.append(path)

    return written


def write_summary_json(planfiles: list[Planfile], output_dir: str | Path) -> Path:
    """Write a JSON summary of all planfiles to *output_dir*/summary.json."""
    out = Path(output_dir)
    out.mkdir(parents=True, exist_ok=True)
    summary_path = out / "summary.json"
    data = [pf.model_dump(mode="json") for pf in planfiles]
    summary_path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")
    return summary_path
