from pathlib import Path

from promptspec_harness import (
    QualityMetrics,
    evaluate_quality_gate,
    export_quality_report,
    prompt_version_diff,
)


def test_quality_gate_passes_clean_metrics() -> None:
    result = evaluate_quality_gate(
        QualityMetrics(
            slot_coverage=1.0,
            render_fidelity=1.0,
            conflict_count=0,
            ambiguity_count=0,
            over_generation_count=0,
            required_tests_pass=True,
        )
    )

    assert result.status == "pass"
    assert result.failed_rules == []


def test_quality_gate_fails_unresolved_blockers() -> None:
    result = evaluate_quality_gate(
        QualityMetrics(
            slot_coverage=1.0,
            render_fidelity=1.0,
            conflict_count=0,
            ambiguity_count=0,
            over_generation_count=0,
            required_tests_pass=True,
            unresolved_blockers=["M6"],
        )
    )

    assert result.status == "fail"
    assert "unresolved_blockers" in result.failed_rules


def test_quality_report_export(tmp_path: Path) -> None:
    result = evaluate_quality_gate(
        QualityMetrics(
            slot_coverage=1.0,
            render_fidelity=1.0,
            conflict_count=0,
            ambiguity_count=0,
            over_generation_count=0,
            required_tests_pass=True,
        )
    )

    path = export_quality_report(result, tmp_path / "quality.json")

    assert path.exists()


def test_prompt_version_diff() -> None:
    diff = prompt_version_diff("A\nB", "A\nC")

    assert diff == {"removed": ["B"], "added": ["C"]}

