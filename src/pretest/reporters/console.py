"""Console reporter — prints findings to stdout using click styling."""

from __future__ import annotations

import click

from pretest.models.findings import AnalysisReport


def print_report(report: AnalysisReport) -> None:
    """Print a human-readable summary to the terminal."""
    click.echo(click.style("\n=== pretest analysis report ===\n", bold=True))

    # Duplicates
    if report.duplicates:
        click.echo(click.style(f"Duplicate tests ({len(report.duplicates)}):", fg="yellow"))
        for d in report.duplicates:
            click.echo(
                f"  [score={d.score:.2f}] {d.test_a} ↔ {d.test_b}"
            )
    else:
        click.echo(click.style("No duplicate tests found.", fg="green"))

    click.echo()

    # Dead tests
    if report.dead_tests:
        click.echo(click.style(f"Dead tests ({len(report.dead_tests)}):", fg="yellow"))
        for d in report.dead_tests:
            click.echo(f"  {d.node_id}  (unique_lines={d.unique_lines})")
    else:
        click.echo(click.style("No dead tests found.", fg="green"))

    click.echo()

    # Missing tests
    if report.missing_tests:
        click.echo(click.style(f"Missing tests ({len(report.missing_tests)}):", fg="cyan"))
        for m in report.missing_tests:
            priority_color = "red" if m.priority == "high" else "yellow"
            click.echo(
                f"  [{click.style(m.priority.upper(), fg=priority_color)}] "
                f"[{m.test_type}] {m.target}"
            )
    else:
        click.echo(click.style("No missing tests detected.", fg="green"))

    click.echo()

    # Refactor candidates
    if report.refactor_candidates:
        click.echo(
            click.style(f"Refactor candidates ({len(report.refactor_candidates)}):", fg="magenta")
        )
        for r in report.refactor_candidates:
            click.echo(f"  {r.node_id}: {r.reason}")
    else:
        click.echo(click.style("No refactoring needed.", fg="green"))

    click.echo()
