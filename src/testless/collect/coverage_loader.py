"""Load coverage.py JSON output (with --cov-context=test) into a CoverageMap."""

from __future__ import annotations

import json
from pathlib import Path

from testless.models.coverage_map import CoverageMap, FileCoverage


def load_coverage_json(json_path: str | Path) -> CoverageMap:
    """
    Parse a coverage.json file produced by::

        pytest --cov=<pkg> --cov-report=json --cov-context=test

    Returns a :class:`CoverageMap` with per-line, per-test context data.
    """
    path = Path(json_path)
    if not path.exists():
        return CoverageMap()

    with path.open() as fh:
        data = json.load(fh)

    cmap = CoverageMap()
    for file_path, file_data in data.get("files", {}).items():
        fc = FileCoverage(path=file_path)

        # executed_lines holds lines touched in the current context
        contexts: dict[str, list[int]] = file_data.get("contexts", {})
        # contexts is {context_name: [line_numbers]}
        for context, lines in contexts.items():
            # context looks like "tests/test_foo.py::test_bar|run"
            # strip the phase suffix (|run, |setup, |teardown)
            node_id = context.split("|")[0] if "|" in context else context
            for ln in lines:
                fc.line_to_tests.setdefault(ln, [])
                if node_id not in fc.line_to_tests[ln]:
                    fc.line_to_tests[ln].append(node_id)

        if fc.line_to_tests:
            cmap.files[file_path] = fc

    return cmap
