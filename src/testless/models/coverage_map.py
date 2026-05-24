"""Model for coverage context maps produced by coverage.py --cov-context=test."""

from __future__ import annotations

from pydantic import BaseModel, Field


class FileCoverage(BaseModel):
    """Coverage data for a single source file."""

    path: str
    # Mapping from line number to list of test node IDs that executed it
    line_to_tests: dict[int, list[str]] = Field(default_factory=dict)

    def lines_covered_by(self, node_id: str) -> set[int]:
        """Return set of lines covered by the given test."""
        return {ln for ln, tests in self.line_to_tests.items() if node_id in tests}

    def unique_lines_for(self, node_id: str, all_node_ids: list[str]) -> set[int]:
        """Lines covered only by *node_id* and by no other test in the list."""
        others = set(all_node_ids) - {node_id}
        covered = self.lines_covered_by(node_id)
        unique = {
            ln
            for ln in covered
            if not any(other in self.line_to_tests.get(ln, []) for other in others)
        }
        return unique


class CoverageMap(BaseModel):
    """Aggregated per-context coverage map for the whole project."""

    files: dict[str, FileCoverage] = Field(default_factory=dict)

    def coverage_for_test(self, node_id: str) -> dict[str, set[int]]:
        """Return {filename: {lines}} covered by a single test."""
        result: dict[str, set[int]] = {}
        for path, fc in self.files.items():
            lines = fc.lines_covered_by(node_id)
            if lines:
                result[path] = lines
        return result

    def overlap(self, node_a: str, node_b: str) -> float:
        """Jaccard overlap of coverage between two tests (0–1)."""
        lines_a: set[tuple[str, int]] = set()
        lines_b: set[tuple[str, int]] = set()
        for path, fc in self.files.items():
            for ln in fc.lines_covered_by(node_a):
                lines_a.add((path, ln))
            for ln in fc.lines_covered_by(node_b):
                lines_b.add((path, ln))
        if not lines_a and not lines_b:
            return 0.0
        intersection = lines_a & lines_b
        union = lines_a | lines_b
        return len(intersection) / len(union) if union else 0.0
