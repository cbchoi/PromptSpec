"""Ralph Loop task and acceptance helpers."""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

from promptspec_model import RalphTask, TestReport


@dataclass(frozen=True)
class RalphPaths:
    root: Path = Path(".")

    @property
    def ralph_dir(self) -> Path:
        return self.root / "ralph"

    @property
    def task_list(self) -> Path:
        return self.ralph_dir / "task_list.json"

    @property
    def progress(self) -> Path:
        return self.ralph_dir / "progress.txt"

    @property
    def acceptance_gate(self) -> Path:
        return self.ralph_dir / "acceptance_gate.md"

    @property
    def iteration_log(self) -> Path:
        return self.ralph_dir / "iteration_log.md"

    @property
    def failure_reports(self) -> Path:
        return self.root / "reports/ralph"


def task_from_requirement(requirement_id: str, title: str, test_command: str) -> RalphTask:
    return RalphTask(
        id=requirement_id,
        title=title,
        status="pending",
        source_doc="docs/SRS.md",
        acceptance_criteria=[f"{requirement_id} is implemented and tested"],
        test_commands=[test_command],
        dependencies=[],
    )


def generate_task_list(tasks: list[RalphTask]) -> dict[str, list[dict[str, object]]]:
    return {"tasks": [task.model_dump() for task in tasks]}


def load_tasks(path: Path) -> list[RalphTask]:
    payload = json.loads(path.read_text())
    return [
        RalphTask.model_validate(_canonical_task_payload(item))
        for item in payload.get("tasks", [])
    ]


def write_tasks(path: Path, tasks: list[RalphTask]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(generate_task_list(tasks), indent=2))


def _canonical_task_payload(item: object) -> dict[str, object]:
    if not isinstance(item, dict):
        raise ValueError("Ralph task payload must be an object")
    allowed = {
        "id",
        "title",
        "status",
        "source_doc",
        "acceptance_criteria",
        "test_commands",
        "dependencies",
    }
    return {key: value for key, value in item.items() if key in allowed}


def select_next_task(tasks: list[RalphTask]) -> RalphTask | None:
    completed = {task.id for task in tasks if task.status == "completed"}
    for task in tasks:
        if task.status != "pending":
            continue
        if all(dependency in completed for dependency in task.dependencies):
            return task
    return None


def validate_task_contract(task: RalphTask) -> TestReport:
    passed = bool(task.acceptance_criteria) and bool(task.test_commands)
    return TestReport(
        report_id=f"ralph_{task.id}",
        suite="ralph",
        status="pass" if passed else "fail",
        commands=task.test_commands,
        artifacts=[],
    )


def append_acceptance_evidence(
    path: Path,
    task_id: str,
    evidence: str,
    commit: str,
    status: str = "pass",
) -> None:
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            "# Ralph Acceptance Gate\n\n"
            "## Evidence Log\n\n"
            "| Task | Status | Evidence | Commit |\n"
            "|---|---|---|---|\n"
        )
    with path.open("a") as handle:
        handle.write(f"| {task_id} | {status} | {evidence} | {commit} |\n")


def write_failure_report(paths: RalphPaths, task_id: str, reason: str) -> Path:
    paths.failure_reports.mkdir(parents=True, exist_ok=True)
    path = paths.failure_reports / f"failure_{task_id}.md"
    path.write_text(f"# Ralph Failure {task_id}\n\n{reason}\n")
    return path
