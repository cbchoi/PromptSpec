from pathlib import Path

from promptspec_harness import load_test_case


def test_load_test_case_from_json() -> None:
    case = load_test_case(Path("fixtures/scenario/pass_case.json"))

    assert case.id == "scenario_pass_case"
    assert case.prompt_spec.id == "spec_001"

