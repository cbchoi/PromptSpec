import pytest
from promptspec_model import ValidationIssue, ValidationMetrics, ValidationReport
from pydantic import ValidationError


def metrics() -> ValidationMetrics:
    return ValidationMetrics(
        slot_coverage=1.0,
        conflict_count=0,
        critical_over_generation=0,
        meaning_schema_valid=True,
    )


def test_validation_report_accepts_canonical_fields() -> None:
    report = ValidationReport(
        spec_id="spec_001",
        status="fail",
        issues=[
            ValidationIssue(
                code="MISSING_SLOT",
                severity="critical",
                slot_key="audience",
                message="Required slot was not represented.",
            )
        ],
        metrics=metrics(),
    )

    assert report.status == "fail"
    assert report.issues[0].severity == "critical"
    assert report.metrics.slot_coverage == 1.0


def test_validation_report_rejects_invalid_status() -> None:
    with pytest.raises(ValidationError):
        ValidationReport(spec_id="spec_001", status="unknown", metrics=metrics())


def test_validation_issue_rejects_invalid_severity() -> None:
    with pytest.raises(ValidationError):
        ValidationIssue(code="MISSING_SLOT", severity="severe", message="x")


def test_validation_metrics_reject_invalid_slot_coverage() -> None:
    with pytest.raises(ValidationError):
        ValidationMetrics(
            slot_coverage=1.1,
            conflict_count=0,
            critical_over_generation=0,
            meaning_schema_valid=True,
        )

