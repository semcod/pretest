"""Markdown reporter — writes findings as a Markdown file."""

from __future__ import annotations

from pathlib import Path

from pretest.models.findings import AnalysisReport


def write_markdown_report(report: AnalysisReport, output_path: str | Path) -> Path:
    """Write a Markdown report to *output_path*."""
    out = Path(output_path)
    out.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = ["# pretest Analysis Report\n"]

    lines.append("## Duplicate Tests\n")
    if report.duplicates:
        lines.append("| Score | Test A | Test B |")
        lines.append("|-------|--------|--------|")
        for d in report.duplicates:
            lines.append(f"| {d.score:.2f} | `{d.test_a}` | `{d.test_b}` |")
    else:
        lines.append("_No duplicates found._")
    lines.append("")

    lines.append("## Dead Tests\n")
    if report.dead_tests:
        lines.append("| Test | Unique Lines | Total Lines |")
        lines.append("|------|-------------|-------------|")
        for d in report.dead_tests:
            lines.append(f"| `{d.node_id}` | {d.unique_lines} | {d.total_lines} |")
    else:
        lines.append("_No dead tests found._")
    lines.append("")

    lines.append("## Missing Tests\n")
    if report.missing_tests:
        lines.append("| Priority | Type | Target | Description |")
        lines.append("|----------|------|--------|-------------|")
        for m in report.missing_tests:
            lines.append(f"| {m.priority} | {m.test_type} | `{m.target}` | {m.description} |")
    else:
        lines.append("_No missing tests detected._")
    lines.append("")

    lines.append("## Refactor Candidates\n")
    if report.refactor_candidates:
        lines.append("| Test | Reason |")
        lines.append("|------|--------|")
        for r in report.refactor_candidates:
            lines.append(f"| `{r.node_id}` | {r.reason} |")
    else:
        lines.append("_No refactoring needed._")
    lines.append("")

    out.write_text("\n".join(lines), encoding="utf-8")
    return out
