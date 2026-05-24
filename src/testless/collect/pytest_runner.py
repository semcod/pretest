"""Run pytest and collect test metadata via subprocess."""

from __future__ import annotations

import json
import subprocess
import sys
from pathlib import Path

from testless.models.findings import TestMeta


def run_pytest(
    packages: list[str],
    test_dirs: list[str],
    coverage_dir: str = ".coverage_data",
    extra_args: list[str] | None = None,
) -> tuple[list[TestMeta], Path]:
    """
    Run pytest with coverage contexts enabled and collect test metadata.

    Returns a tuple of (list[TestMeta], coverage_json_path).
    The coverage JSON is written to *coverage_dir*/coverage.json.
    """
    cov_dir = Path(coverage_dir)
    cov_dir.mkdir(parents=True, exist_ok=True)
    json_path = cov_dir / "coverage.json"

    cov_source = ",".join(packages) if packages else "."
    cmd = [
        sys.executable,
        "-m",
        "pytest",
        "--tb=no",
        "-q",
        "--json-report",
        f"--json-report-file={cov_dir / 'report.json'}",
        f"--cov={cov_source}",
        f"--cov-report=json:{json_path}",
        "--cov-context=test",
    ]
    cmd += extra_args or []
    cmd += test_dirs

    result = subprocess.run(cmd, capture_output=False, text=True)  # noqa: S603

    # Parse the pytest JSON report if available
    report_path = cov_dir / "report.json"
    tests: list[TestMeta] = []
    if report_path.exists():
        tests = _parse_report(report_path)

    return tests, json_path


def _parse_report(report_path: Path) -> list[TestMeta]:
    """Parse pytest-json-report output into TestMeta objects."""
    with report_path.open() as fh:
        data = json.load(fh)

    tests: list[TestMeta] = []
    for test in data.get("tests", []):
        node_id = test.get("nodeid", "")
        parts = node_id.split("::")
        file_path = parts[0] if parts else ""
        name = "::".join(parts[1:]) if len(parts) > 1 else node_id
        tests.append(
            TestMeta(
                node_id=node_id,
                file=file_path,
                name=name,
                duration=test.get("call", {}).get("duration", 0.0),
                status=test.get("outcome", "unknown"),
            )
        )
    return tests
