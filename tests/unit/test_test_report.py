import pytest
from promptspec_model import TestReport as PromptspecTestReport
from pydantic import ValidationError


def test_test_report_accepts_canonical_fields() -> None:
    report = PromptspecTestReport(
        report_id="report_001",
        suite="unit",
        status="pass",
        commands=["python -m pytest tests/unit"],
        artifacts=["reports/tests/report_001.json"],
    )

    assert report.report_id == "report_001"
    assert report.suite == "unit"
    assert report.status == "pass"
    assert report.commands == ["python -m pytest tests/unit"]
    assert report.artifacts == ["reports/tests/report_001.json"]


def test_test_report_defaults_commands_and_artifacts() -> None:
    report = PromptspecTestReport(report_id="report_001", suite="ralph", status="fail")

    assert report.commands == []
    assert report.artifacts == []


def test_test_report_rejects_invalid_suite() -> None:
    with pytest.raises(ValidationError):
        PromptspecTestReport(report_id="report_001", suite="smoke", status="pass")


def test_test_report_rejects_invalid_status() -> None:
    with pytest.raises(ValidationError):
        PromptspecTestReport(report_id="report_001", suite="unit", status="unknown")
