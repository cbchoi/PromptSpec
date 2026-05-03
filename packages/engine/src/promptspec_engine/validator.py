"""Deterministic validation for rendered prompts."""

from __future__ import annotations

import string

from promptspec_model import (
    MeaningReport,
    PromptSpec,
    RenderedPrompt,
    ValidationIssue,
    ValidationMetrics,
    ValidationReport,
)

AMBIGUITY_MARKERS = ("maybe", "possibly", "unclear", "ambiguous", "perhaps")


def validate_prompt(
    spec: PromptSpec,
    rendered: RenderedPrompt,
    meaning_report: MeaningReport | None = None,
) -> ValidationReport:
    issues: list[ValidationIssue] = []
    span_by_key = {span.slot_key: span for span in rendered.spans}

    missing_count = 0
    for slot in spec.slots:
        span = span_by_key.get(slot.key)
        if slot.required and span is None:
            missing_count += 1
            issues.append(
                ValidationIssue(
                    code="MISSING_SLOT",
                    severity="critical",
                    slot_key=slot.key,
                    message="Required slot was not represented in rendered prompt.",
                )
            )
        elif span is not None and span.text != slot.value:
            issues.append(
                ValidationIssue(
                    code="RENDER_OMISSION",
                    severity="critical",
                    slot_key=slot.key,
                    message="Rendered span text does not match source slot value.",
                )
            )

    conflict_count = _append_declared_conflicts(spec, issues)
    critical_over_generation = _append_over_generation(spec, rendered, issues)
    _append_ambiguity(rendered, issues)

    if meaning_report is not None and meaning_report.spec_id != spec.id:
        issues.append(
            ValidationIssue(
                code="SCHEMA_VIOLATION",
                severity="critical",
                message="MeaningReport spec_id does not match PromptSpec id.",
            )
        )

    represented = len([slot for slot in spec.slots if slot.key in span_by_key])
    slot_coverage = represented / len(spec.slots) if spec.slots else 1.0
    status: str = "fail" if any(issue.severity == "critical" for issue in issues) else "pass"

    return ValidationReport(
        spec_id=spec.id,
        status="fail" if status == "fail" else "pass",
        issues=issues,
        metrics=ValidationMetrics(
            slot_coverage=slot_coverage,
            conflict_count=conflict_count,
            critical_over_generation=critical_over_generation,
            meaning_schema_valid=meaning_report is None or meaning_report.spec_id == spec.id,
        ),
    )


def _append_declared_conflicts(spec: PromptSpec, issues: list[ValidationIssue]) -> int:
    conflicts = spec.metadata.get("conflicts", [])
    if not isinstance(conflicts, list):
        return 0

    count = 0
    active_keys = {slot.key for slot in spec.slots}
    for conflict in conflicts:
        if not isinstance(conflict, dict):
            continue
        keys = conflict.get("slot_keys", [])
        if not isinstance(keys, list):
            continue
        if all(key in active_keys for key in keys):
            count += 1
            issues.append(
                ValidationIssue(
                    code="SEMANTIC_CONFLICT",
                    severity="critical",
                    message=str(conflict.get("message", "Active slots conflict.")),
                )
            )
    return count


def _append_over_generation(
    spec: PromptSpec,
    rendered: RenderedPrompt,
    issues: list[ValidationIssue],
) -> int:
    remainder = rendered.text
    for slot in spec.slots:
        remainder = remainder.replace(slot.value, "", 1)

    if remainder.strip(string.whitespace + string.punctuation):
        issues.append(
            ValidationIssue(
                code="OVER_GENERATION",
                severity="critical",
                message="Rendered prompt contains meaning not present in source slots.",
            )
        )
        return 1
    return 0


def _append_ambiguity(rendered: RenderedPrompt, issues: list[ValidationIssue]) -> None:
    lowered = rendered.text.lower()
    if any(marker in lowered for marker in AMBIGUITY_MARKERS):
        issues.append(
            ValidationIssue(
                code="AMBIGUOUS_OUTPUT",
                severity="warning",
                message="Rendered prompt contains ambiguous wording.",
            )
        )
