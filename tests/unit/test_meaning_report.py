import pytest
from promptspec_model import MeaningReport
from pydantic import ValidationError


def test_meaning_report_accepts_canonical_fields() -> None:
    report = MeaningReport(
        spec_id="spec_001",
        schema_version=1,
        meaning={"audience": "senior backend engineers"},
        uncertainties=["tone"],
        raw_model='{"audience":"senior backend engineers"}',
    )

    assert report.spec_id == "spec_001"
    assert report.schema_version == 1
    assert report.meaning == {"audience": "senior backend engineers"}
    assert report.uncertainties == ["tone"]
    assert report.raw_model is not None


def test_meaning_report_defaults_uncertainties_and_raw_model() -> None:
    report = MeaningReport(spec_id="spec_001", meaning={})

    assert report.schema_version == 1
    assert report.uncertainties == []
    assert report.raw_model is None


def test_meaning_report_rejects_non_object_meaning() -> None:
    with pytest.raises(ValidationError):
        MeaningReport(spec_id="spec_001", meaning=["not", "object"])

