"""LLM-ready prompt fragments embedded in planfile hints."""

from __future__ import annotations

from pretest.models.planfile import Planfile, PlanfileKind

_PROMPTS: dict[PlanfileKind, str] = {
    PlanfileKind.duplicate: (
        "You are a Python test refactoring assistant. "
        "Given the two test functions below, determine which one should be removed. "
        "Prefer keeping the test with the more descriptive name and broader assertion set. "
        "Return a minimal diff."
    ),
    PlanfileKind.dead: (
        "You are a Python test hygiene assistant. "
        "The following test contributes zero unique coverage. "
        "Decide whether to remove it or merge it into an existing test. "
        "Justify your choice."
    ),
    PlanfileKind.missing: (
        "You are a Python test author. "
        "Based on the description below, implement the suggested tests. "
        "Follow the existing project style and use pytest fixtures where possible."
    ),
    PlanfileKind.refactor: (
        "You are a Python test refactoring assistant. "
        "Refactor the following test to address the listed issues "
        "without changing the coverage or semantics of the assertions."
    ),
    PlanfileKind.testql: (
        "You are a database testing specialist. "
        "Implement the TestQL-style SQL contract tests described below. "
        "Ensure each query is tested with at least one boundary value and one error case."
    ),
}


def attach_prompt(planfile: Planfile) -> Planfile:
    """Return a copy of *planfile* with the LLM system prompt attached to llm_hints."""
    prompt = _PROMPTS.get(planfile.kind, "")
    updated_hints = {**planfile.llm_hints, "system_prompt": prompt}
    return planfile.model_copy(update={"llm_hints": updated_hints})
