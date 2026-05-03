from pathlib import Path

from promptspec_harness import HarnessRunner
from promptspec_harness.models import PromptTestCase
from promptspec_model import PromptSlot, PromptSpec, PromptStrategy


def test_harness_runner_runs_scenario_suite(tmp_path: Path) -> None:
    runner = HarnessRunner(Path("fixtures"), tmp_path)

    report = runner.run_suite("scenario")

    assert report.status == "pass"
    assert report.suite == "scenario"
    assert (tmp_path / "scenario_pass_case.json").exists()
    assert (tmp_path / "scenario_suite.json").exists()


def test_harness_runner_writes_failed_case_report(tmp_path: Path) -> None:
    runner = HarnessRunner(Path("fixtures"), tmp_path)
    strategy = PromptStrategy(
        render_strategy="plain",
        validation_strategy="strict",
        inspection_strategy="schema_bound",
    )
    case = PromptTestCase(
        id="expected_failure",
        suite="scenario",
        prompt_spec=PromptSpec(
            id="spec_failure",
            title="Failure",
            strategy=strategy,
            slots=[PromptSlot(key="task", type="task", value="Summarize.")],
        ),
        expected_status="pass",
        expected_text="Different text",
    )

    passed, artifact = runner.run_case(case)

    assert passed is False
    assert artifact.exists()
