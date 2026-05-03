"""Quality gate aggregation and release reporting."""

from __future__ import annotations

import json
from pathlib import Path

from pydantic import BaseModel, ConfigDict, Field


class QualityMetrics(BaseModel):
    model_config = ConfigDict(extra="forbid")

    slot_coverage: float = Field(ge=0.0, le=1.0)
    render_fidelity: float = Field(ge=0.0, le=1.0)
    conflict_count: int = Field(ge=0)
    ambiguity_count: int = Field(ge=0)
    over_generation_count: int = Field(ge=0)
    required_tests_pass: bool
    unresolved_blockers: list[str] = Field(default_factory=list)


class QualityGateResult(BaseModel):
    model_config = ConfigDict(extra="forbid")

    status: str
    metrics: QualityMetrics
    failed_rules: list[str] = Field(default_factory=list)


def evaluate_quality_gate(metrics: QualityMetrics) -> QualityGateResult:
    failed_rules: list[str] = []
    if metrics.slot_coverage < 1.0:
        failed_rules.append("slot_coverage")
    if metrics.render_fidelity < 1.0:
        failed_rules.append("render_fidelity")
    if metrics.conflict_count != 0:
        failed_rules.append("conflict_count")
    if metrics.over_generation_count != 0:
        failed_rules.append("over_generation_count")
    if not metrics.required_tests_pass:
        failed_rules.append("required_tests_pass")
    if metrics.unresolved_blockers:
        failed_rules.append("unresolved_blockers")

    return QualityGateResult(
        status="fail" if failed_rules else "pass",
        metrics=metrics,
        failed_rules=failed_rules,
    )


def export_quality_report(result: QualityGateResult, path: Path) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(result.model_dump(), indent=2))
    return path


def prompt_version_diff(before: str, after: str) -> dict[str, list[str]]:
    before_lines = before.splitlines()
    after_lines = after.splitlines()
    return {
        "removed": [line for line in before_lines if line not in after_lines],
        "added": [line for line in after_lines if line not in before_lines],
    }

