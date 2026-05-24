"""Models for analysis findings."""

from __future__ import annotations

from pydantic import BaseModel, Field


class TestMeta(BaseModel):
    """Metadata about a single test collected from pytest."""

    node_id: str
    file: str
    name: str
    duration: float = 0.0
    status: str = "unknown"
    markers: list[str] = Field(default_factory=list)
    fixtures: list[str] = Field(default_factory=list)


class DuplicateFinding(BaseModel):
    """Two tests that are likely duplicates."""

    test_a: str
    test_b: str
    score: float
    coverage_overlap: float = 0.0
    ast_similarity: float = 0.0
    fixture_overlap: float = 0.0
    name_similarity: float = 0.0
    recommendation: str = "remove weaker test"


class DeadTestFinding(BaseModel):
    """A test that contributes no unique coverage."""

    node_id: str
    file: str
    unique_lines: int = 0
    total_lines: int = 0
    reason: str = "no unique coverage"


class MissingTestFinding(BaseModel):
    """A suggested missing test for an endpoint or module."""

    target: str
    test_type: str
    description: str
    priority: str = "medium"
    suggested_file: str | None = None


class RefactorFinding(BaseModel):
    """A test that should be refactored."""

    node_id: str
    file: str
    reason: str
    details: str = ""


class AnalysisReport(BaseModel):
    """Full report produced by pretest analyze."""

    duplicates: list[DuplicateFinding] = Field(default_factory=list)
    dead_tests: list[DeadTestFinding] = Field(default_factory=list)
    missing_tests: list[MissingTestFinding] = Field(default_factory=list)
    refactor_candidates: list[RefactorFinding] = Field(default_factory=list)
    tests: list[TestMeta] = Field(default_factory=list)
