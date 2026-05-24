"""Detect tests that contribute no unique coverage."""

from __future__ import annotations

from pretest.models.coverage_map import CoverageMap
from pretest.models.findings import DeadTestFinding, TestMeta


def find_dead_tests(
    tests: list[TestMeta],
    cov_map: CoverageMap,
    min_unique_lines: int = 1,
) -> list[DeadTestFinding]:
    """
    Return tests whose unique coverage falls below *min_unique_lines*.

    A test is considered "dead" if every line it touches is already covered
    by at least one other test.
    """
    all_node_ids = [t.node_id for t in tests]
    findings: list[DeadTestFinding] = []

    for test in tests:
        total_lines = 0
        unique_lines = 0

        for fc in cov_map.files.values():
            covered = fc.lines_covered_by(test.node_id)
            unique = fc.unique_lines_for(test.node_id, all_node_ids)
            total_lines += len(covered)
            unique_lines += len(unique)

        if total_lines > 0 and unique_lines < min_unique_lines:
            findings.append(
                DeadTestFinding(
                    node_id=test.node_id,
                    file=test.file,
                    unique_lines=unique_lines,
                    total_lines=total_lines,
                    reason="no unique coverage",
                )
            )

    return findings
