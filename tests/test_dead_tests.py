"""Tests for dead_tests analyzer."""

from __future__ import annotations

from pretest.analyze.dead_tests import find_dead_tests
from pretest.models.coverage_map import CoverageMap, FileCoverage
from pretest.models.findings import TestMeta


def _make_tests(*node_ids: str) -> list[TestMeta]:
    return [
        TestMeta(node_id=nid, file=nid.split("::")[0], name=nid.split("::")[-1])
        for nid in node_ids
    ]


def test_no_dead_tests_when_all_have_unique_coverage():
    fc = FileCoverage(path="src/app.py", line_to_tests={1: ["tests/a.py::test_a"], 2: ["tests/a.py::test_b"]})
    cmap = CoverageMap(files={"src/app.py": fc})
    tests = _make_tests("tests/a.py::test_a", "tests/a.py::test_b")
    result = find_dead_tests(tests, cmap)
    assert result == []


def test_dead_test_detected():
    # test_b covers only line 1, which is also covered by test_a
    fc = FileCoverage(
        path="src/app.py",
        line_to_tests={1: ["tests/a.py::test_a", "tests/a.py::test_b"]},
    )
    cmap = CoverageMap(files={"src/app.py": fc})
    tests = _make_tests("tests/a.py::test_a", "tests/a.py::test_b")
    result = find_dead_tests(tests, cmap, min_unique_lines=1)
    dead_ids = {d.node_id for d in result}
    # Both tests have 0 unique lines (each line covered by the other)
    assert "tests/a.py::test_a" in dead_ids
    assert "tests/a.py::test_b" in dead_ids


def test_test_with_no_coverage_not_flagged():
    # test with no coverage entries — should not be flagged (total_lines = 0)
    cmap = CoverageMap(files={})
    tests = _make_tests("tests/a.py::test_orphan")
    result = find_dead_tests(tests, cmap, min_unique_lines=1)
    assert result == []
