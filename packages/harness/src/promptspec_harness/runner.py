"""Prompt test harness runner."""

from __future__ import annotations

from pathlib import Path

from promptspec_engine import render_prompt, resolve_prompt_spec, validate_prompt
from promptspec_model import MeaningReport, TestReport, TestSuite

from promptspec_harness.comparator import compare_meaning
from promptspec_harness.loader import load_test_cases
from promptspec_harness.models import PromptTestCase
from promptspec_harness.reporting import write_test_report


class HarnessRunner:
    """Runs prompt test fixtures through resolve, render, validate, and compare."""

    def __init__(
        self,
        fixtures_dir: Path = Path("fixtures"),
        reports_dir: Path = Path("reports/tests"),
    ) -> None:
        self.fixtures_dir = fixtures_dir
        self.reports_dir = reports_dir

    def run_suite(self, suite: TestSuite) -> TestReport:
        cases = load_test_cases(self.fixtures_dir / suite)
        failed: list[str] = []
        artifacts: list[str] = []

        for case in cases:
            case_passed, artifact = self.run_case(case)
            artifacts.append(str(artifact))
            if not case_passed:
                failed.append(case.id)

        report = TestReport(
            report_id=f"{suite}_suite",
            suite=suite,
            status="fail" if failed else "pass",
            commands=[f"python harness.py run --suite {suite}"],
            artifacts=artifacts,
        )
        write_test_report(report, self.reports_dir)
        return report

    def run_case(self, case: PromptTestCase) -> tuple[bool, Path]:
        resolved = resolve_prompt_spec(case.prompt_spec, case.parents)
        rendered = render_prompt(resolved)
        meaning = (
            MeaningReport(spec_id=resolved.id, meaning=case.expected_meaning)
            if case.expected_meaning is not None
            else None
        )
        validation = validate_prompt(resolved, rendered, meaning)
        meaning_comparison = compare_meaning(
            case.expected_meaning,
            meaning.meaning if meaning is not None else None,
        )

        text_matches = case.expected_text is None or rendered.text == case.expected_text
        actual_status = (
            "pass"
            if validation.status == "pass" and meaning_comparison.status == "pass" and text_matches
            else "fail"
        )
        passed = actual_status == case.expected_status
        report = TestReport(
            report_id=case.id,
            suite=case.suite,
            status="pass" if passed else "fail",
            commands=[f"prompt case {case.id}"],
            artifacts=[],
        )
        artifact = write_test_report(report, self.reports_dir)
        return passed, artifact
