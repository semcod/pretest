"""Pydantic models for planfile tickets."""

from __future__ import annotations

from enum import Enum
from typing import Any

import yaml
from pydantic import BaseModel, Field


class RiskLevel(str, Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class PlanfileKind(str, Enum):
    duplicate = "duplicate"
    dead = "dead"
    missing = "missing"
    refactor = "refactor"
    testql = "testql"


class PlanfileEvidence(BaseModel):
    """Supporting evidence for the ticket."""

    description: str
    score: float | None = None
    files: list[str] = Field(default_factory=list)


class PlanfileImpact(BaseModel):
    risk: RiskLevel = RiskLevel.low
    expected_gains: list[str] = Field(default_factory=list)


class PlanfileTask(BaseModel):
    description: str
    file: str | None = None


class Planfile(BaseModel):
    """A single LLM-ready ticket in planfile format."""

    version: str = "1"
    kind: PlanfileKind
    id: str
    title: str
    goal: str
    context: dict[str, Any] = Field(default_factory=dict)
    evidence: list[PlanfileEvidence] = Field(default_factory=list)
    impact: PlanfileImpact = Field(default_factory=PlanfileImpact)
    tasks: list[PlanfileTask] = Field(default_factory=list)
    acceptance_criteria: list[str] = Field(default_factory=list)
    artifacts: list[str] = Field(default_factory=list)
    llm_hints: dict[str, Any] = Field(default_factory=lambda: {"style": "minimal change", "safe_refactor": True})

    def to_yaml(self) -> str:
        """Serialize to YAML string."""
        data = self.model_dump(mode="json")
        return yaml.dump(data, sort_keys=False, allow_unicode=True)

    @classmethod
    def from_yaml(cls, text: str) -> "Planfile":
        """Deserialize from YAML string."""
        data = yaml.safe_load(text)
        return cls(**data)
