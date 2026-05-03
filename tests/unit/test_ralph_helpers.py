from pathlib import Path

from promptspec_harness import (
    RalphPaths,
    append_acceptance_evidence,
    generate_task_list,
    load_tasks,
    select_next_task,
    task_from_requirement,
    validate_task_contract,
    write_failure_report,
    write_tasks,
)
from promptspec_model import RalphTask


def test_generate_and_load_task_list(tmp_path: Path) -> None:
    task = task_from_requirement("F9.1", "Generate Ralph tasks", "pytest")
    path = tmp_path / "ralph/task_list.json"

    write_tasks(path, [task])

    assert generate_task_list([task])["tasks"][0]["id"] == "F9.1"
    assert load_tasks(path)[0].id == "F9.1"


def test_select_next_task_respects_dependencies() -> None:
    tasks = [
        RalphTask(
            id="T1",
            title="Done",
            status="completed",
            source_doc="docs/SRS.md",
            acceptance_criteria=["done"],
            test_commands=["pytest"],
        ),
        RalphTask(
            id="T2",
            title="Next",
            status="pending",
            source_doc="docs/SRS.md",
            acceptance_criteria=["next"],
            test_commands=["pytest"],
            dependencies=["T1"],
        ),
    ]

    selected = select_next_task(tasks)

    assert selected is not None
    assert selected.id == "T2"


def test_validate_task_contract() -> None:
    task = task_from_requirement("F9.2", "Validate task contract", "pytest")

    report = validate_task_contract(task)

    assert report.status == "pass"
    assert report.suite == "ralph"


def test_acceptance_evidence_and_failure_report(tmp_path: Path) -> None:
    paths = RalphPaths(root=tmp_path)

    append_acceptance_evidence(paths.acceptance_gate, "T1", "pytest passed", "abc123")
    failure_path = write_failure_report(paths, "T2", "tests failed")

    assert "pytest passed" in paths.acceptance_gate.read_text()
    assert failure_path.name == "failure_T2.md"
    assert "tests failed" in failure_path.read_text()
