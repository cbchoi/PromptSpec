"""FastAPI application for PromptSpec."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Protocol

from fastapi import FastAPI
from promptspec_engine import render_prompt, resolve_prompt_spec, validate_prompt
from promptspec_harness.runner import HarnessRunner
from promptspec_model import (
    MeaningReport,
    PromptSpec,
    RenderedPrompt,
    TestReport,
    TestSuite,
    ValidationReport,
)
from pydantic import BaseModel, ConfigDict

from promptspec_api.errors import error_response, value_error_handler
from promptspec_api.settings import AppSettings, SettingsRepository


class ValidateRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    prompt_spec: PromptSpec
    rendered_prompt: RenderedPrompt
    meaning_report: MeaningReport | None = None


class TestRunRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    suite: TestSuite
    test_ids: list[str] = []


class RalphCheckRequest(BaseModel):
    model_config = ConfigDict(extra="forbid")

    task_id: str


class Inspector(Protocol):
    def inspect(self, rendered_prompt: RenderedPrompt) -> MeaningReport: ...


class EchoInspector:
    def inspect(self, rendered_prompt: RenderedPrompt) -> MeaningReport:
        return MeaningReport(
            spec_id=rendered_prompt.spec_id,
            meaning={"text": rendered_prompt.text},
            uncertainties=[],
            raw_model=None,
        )


def create_app(
    settings_repo: SettingsRepository | None = None,
    harness_runner: HarnessRunner | None = None,
    inspector: Inspector | None = None,
    root: Path = Path("."),
) -> FastAPI:
    app = FastAPI(title="PromptSpec API")
    app.add_exception_handler(ValueError, value_error_handler)

    repo = settings_repo or SettingsRepository()
    runner = harness_runner or HarnessRunner(root / "fixtures", root / "reports/tests")
    prompt_inspector = inspector or EchoInspector()

    @app.post("/api/prompts/resolve", response_model=PromptSpec)
    def resolve_endpoint(prompt_spec: PromptSpec) -> PromptSpec:
        return resolve_prompt_spec(prompt_spec)

    @app.post("/api/prompts/render", response_model=RenderedPrompt)
    def render_endpoint(prompt_spec: PromptSpec) -> RenderedPrompt:
        return render_prompt(prompt_spec)

    @app.post("/api/prompts/inspect", response_model=MeaningReport)
    def inspect_endpoint(rendered_prompt: RenderedPrompt) -> MeaningReport:
        return prompt_inspector.inspect(rendered_prompt)

    @app.post("/api/prompts/validate", response_model=ValidationReport)
    def validate_endpoint(payload: ValidateRequest) -> ValidationReport:
        return validate_prompt(
            payload.prompt_spec,
            payload.rendered_prompt,
            payload.meaning_report,
        )

    @app.post("/api/tests/run", response_model=TestReport)
    def tests_run_endpoint(payload: TestRunRequest) -> TestReport:
        return runner.run_suite(payload.suite)

    @app.get("/api/tests/report/{report_id}", response_model=TestReport)
    def tests_report_endpoint(report_id: str) -> TestReport:
        report_path = runner.reports_dir / f"{report_id}.json"
        if not report_path.exists():
            return error_response(404, "NOT_FOUND", f"Report not found: {report_id}")  # type: ignore[return-value]
        return TestReport.model_validate_json(report_path.read_text())

    @app.get("/api/settings", response_model=AppSettings)
    def get_settings_endpoint() -> AppSettings:
        return repo.get()

    @app.put("/api/settings", response_model=AppSettings)
    def put_settings_endpoint(settings: AppSettings) -> AppSettings:
        return repo.update(settings)

    @app.get("/api/ralph/status")
    def ralph_status_endpoint() -> dict[str, Any]:
        task_list_path = root / "ralph/task_list.json"
        progress_path = root / "ralph/progress.txt"
        tasks = json.loads(task_list_path.read_text())["tasks"] if task_list_path.exists() else []
        progress_text = progress_path.read_text() if progress_path.exists() else ""
        return {"tasks": tasks, "progress": _parse_progress(progress_text)}

    @app.post("/api/ralph/check", response_model=TestReport)
    def ralph_check_endpoint(payload: RalphCheckRequest) -> TestReport:
        task_list_path = root / "ralph/task_list.json"
        if not task_list_path.exists():
            return error_response(404, "NOT_FOUND", "Ralph task list not found")  # type: ignore[return-value]
        tasks = json.loads(task_list_path.read_text())["tasks"]
        task = next((item for item in tasks if item["id"] == payload.task_id), None)
        if task is None:
            return error_response(404, "NOT_FOUND", f"Task not found: {payload.task_id}")  # type: ignore[return-value]

        has_contract = bool(task.get("acceptance_criteria")) and bool(task.get("test_commands"))
        return TestReport(
            report_id=f"ralph_{payload.task_id}",
            suite="ralph",
            status="pass" if has_contract else "fail",
            commands=task.get("test_commands", []),
            artifacts=[],
        )

    return app


def _parse_progress(progress_text: str) -> dict[str, list[str] | str | None]:
    sections: dict[str, list[str]] = {
        "completed": [],
        "in_progress": [],
        "blocked": [],
    }
    last_failure: str | None = None
    current: str | None = None
    for line in progress_text.splitlines():
        stripped = line.strip()
        if stripped == "Completed:":
            current = "completed"
        elif stripped == "In Progress:":
            current = "in_progress"
        elif stripped == "Blocked:":
            current = "blocked"
        elif stripped == "Last Failure:":
            current = "last_failure"
        elif stripped.startswith("- "):
            value = stripped[2:]
            if current == "last_failure":
                last_failure = None if value == "None" else value
            elif current in sections and value != "None":
                sections[current].append(value)
    return {**sections, "last_failure": last_failure}


app = create_app()
