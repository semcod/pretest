"""Build Planfile tickets from analysis findings."""

from __future__ import annotations

import uuid

from testless.models.findings import (
    AnalysisReport,
    DeadTestFinding,
    DuplicateFinding,
    MissingTestFinding,
    RefactorFinding,
)
from testless.models.planfile import (
    Planfile,
    PlanfileEvidence,
    PlanfileImpact,
    PlanfileKind,
    PlanfileTask,
    RiskLevel,
)


def _short_id(prefix: str) -> str:
    return f"{prefix}-{uuid.uuid4().hex[:6].upper()}"


def build_duplicate_ticket(finding: DuplicateFinding) -> Planfile:
    short_a = finding.test_a.split("::")[-1]
    short_b = finding.test_b.split("::")[-1]
    return Planfile(
        kind=PlanfileKind.duplicate,
        id=_short_id("DUP"),
        title=f"Remove duplicate test: {short_a} vs {short_b}",
        goal="Reduce test suite redundancy without losing unique coverage",
        context={
            "test_a": finding.test_a,
            "test_b": finding.test_b,
        },
        evidence=[
            PlanfileEvidence(
                description=(
                    f"{short_a} and {short_b} are likely duplicates "
                    f"(score={finding.score:.2f}, "
                    f"coverage_overlap={finding.coverage_overlap:.2f})"
                ),
                score=finding.score,
                files=[finding.test_a.split("::")[0], finding.test_b.split("::")[0]],
            )
        ],
        impact=PlanfileImpact(
            risk=RiskLevel.low,
            expected_gains=["shorter test run time", "reduced maintenance burden"],
        ),
        tasks=[
            PlanfileTask(description=f"Compare {short_a} and {short_b} manually"),
            PlanfileTask(description="Remove the weaker/less descriptive test"),
            PlanfileTask(description="Run the suite and verify no coverage regression"),
        ],
        acceptance_criteria=[
            "No decrease in unique line coverage",
            "All remaining tests pass",
            "Test run time does not increase",
        ],
        artifacts=["diff", "coverage delta"],
    )


def build_dead_test_ticket(finding: DeadTestFinding) -> Planfile:
    short = finding.node_id.split("::")[-1]
    return Planfile(
        kind=PlanfileKind.dead,
        id=_short_id("DEAD"),
        title=f"Remove dead test: {short}",
        goal="Remove test with zero unique coverage to reduce maintenance",
        context={"node_id": finding.node_id, "file": finding.file},
        evidence=[
            PlanfileEvidence(
                description=(
                    f"{short} covers {finding.total_lines} lines "
                    f"but contributes {finding.unique_lines} unique lines. "
                    f"Reason: {finding.reason}"
                ),
                files=[finding.file],
            )
        ],
        impact=PlanfileImpact(
            risk=RiskLevel.low,
            expected_gains=["cleaner test suite", "faster CI"],
        ),
        tasks=[
            PlanfileTask(description=f"Verify that {short} truly adds no unique coverage"),
            PlanfileTask(description="Remove or merge the test"),
            PlanfileTask(description="Re-run coverage to confirm no regression"),
        ],
        acceptance_criteria=[
            "Coverage report unchanged after removal",
            "No other tests broken",
        ],
        artifacts=["coverage diff"],
    )


def build_missing_test_ticket(finding: MissingTestFinding) -> Planfile:
    return Planfile(
        kind=PlanfileKind.missing,
        id=_short_id("MISS"),
        title=f"Add {finding.test_type} test for {finding.target}",
        goal=finding.description,
        context={"target": finding.target, "test_type": finding.test_type},
        evidence=[
            PlanfileEvidence(
                description=finding.description,
                files=[finding.suggested_file] if finding.suggested_file else [],
            )
        ],
        impact=PlanfileImpact(
            risk=RiskLevel.medium if finding.priority != "high" else RiskLevel.high,
            expected_gains=[
                f"improved {finding.test_type} coverage for {finding.target}"
            ],
        ),
        tasks=[
            PlanfileTask(
                description=f"Create {finding.suggested_file or 'suggested test file'}",
                file=finding.suggested_file,
            ),
            PlanfileTask(description=f"Implement {finding.test_type} tests for {finding.target}"),
            PlanfileTask(description="Ensure tests pass in CI"),
        ],
        acceptance_criteria=[
            f"{finding.target} has at least one {finding.test_type} test",
            "Test passes in CI",
        ],
        artifacts=["new test file"],
    )


def build_refactor_ticket(finding: RefactorFinding) -> Planfile:
    short = finding.node_id.split("::")[-1]
    return Planfile(
        kind=PlanfileKind.refactor,
        id=_short_id("REF"),
        title=f"Refactor test: {short}",
        goal="Improve test quality and maintainability",
        context={"node_id": finding.node_id, "file": finding.file},
        evidence=[
            PlanfileEvidence(
                description=finding.reason,
                files=[finding.file],
            )
        ],
        impact=PlanfileImpact(
            risk=RiskLevel.low,
            expected_gains=["more readable tests", "easier maintenance"],
        ),
        tasks=[
            PlanfileTask(description=f"Refactor {short}: {finding.reason}"),
            PlanfileTask(description="Keep same coverage and assertions"),
        ],
        acceptance_criteria=[
            "Test still passes",
            "Coverage unchanged",
            "Addressed refactoring concerns",
        ],
        artifacts=["diff"],
    )


def build_planfiles(report: AnalysisReport) -> list[Planfile]:
    """Convert a full AnalysisReport into a list of Planfile tickets."""
    planfiles: list[Planfile] = []

    for dup in report.duplicates:
        planfiles.append(build_duplicate_ticket(dup))

    for dead in report.dead_tests:
        planfiles.append(build_dead_test_ticket(dead))

    for missing in report.missing_tests:
        planfiles.append(build_missing_test_ticket(missing))

    for refactor in report.refactor_candidates:
        planfiles.append(build_refactor_ticket(refactor))

    return planfiles
