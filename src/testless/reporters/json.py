"""JSON reporter — serializes the full AnalysisReport to JSON."""

from __future__ import annotations

import json
from pathlib import Path

from testless.models.findings import AnalysisReport


def write_json_report(report: AnalysisReport, output_path: str | Path) -> Path:
    """Write the full report as JSON to *output_path*."""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(
        json.dumps(report.model_dump(mode="json"), indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    return out
