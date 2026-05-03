# Milestone Plan

This folder breaks the SRS into implementation milestones and task-level work.
Task IDs are structured so they can later be converted into `ralph/task_list.json`.

## Milestones

| Milestone | Goal |
|---|---|
| M1 Core Contracts | Implement canonical data models and schema validation. |
| M2 Prompt Engine MVP | Implement deterministic slot resolution, rendering, and validation. |
| M3 Test Harness | Make prompt behavior testable through fixtures, runners, and reports. |
| M4 FastAPI Backend | Expose engine and harness behavior through HTTP APIs. |
| M5 Local LLM Meaning Inspector | Add schema-bound local LLM inspection. |
| M6 Web UI Prompt Studio | Build the primary prompt editing and validation workflow. |
| M7 Test Lab and Agent Trace UI | Expose test execution and agent trace inspection. |
| M8 Ralph Loop Integration | Add task generation, progress tracking, acceptance gate, and Ralph dashboard. |
| M9 Desktop Packaging | Package the shared frontend in a Tauri desktop shell. |
| M10 Quality Gate and Release Readiness | Verify full SRS coverage and release quality. |

## M1 Core Contracts

Goal: make the system implementable without schema ambiguity.

Covers:
- F1.2
- F3.2
- F4.2
- F6.4
- F9.2

Tasks:
- M1.T1 Define package layout for shared model code.
- M1.T2 Implement `PromptSlot` model.
- M1.T3 Implement `PromptSpec` model.
- M1.T4 Implement `RenderedPrompt` and `Span` models.
- M1.T5 Implement `MeaningReport`.
- M1.T6 Implement `ValidationReport`.
- M1.T7 Implement `TestReport`.
- M1.T8 Implement `RalphTask`.
- M1.T9 Add JSON schema export for all canonical models.
- M1.T10 Add unit tests for required fields, enums, defaults, and invalid payloads.

Exit criteria:
- All canonical models from `Data_Model.md` exist in code.
- Schema tests pass.

## M2 Prompt Engine MVP

Goal: deterministic slot resolution and rendering.

Covers:
- F1.1
- F1.3
- F2.1-F2.4
- F3.1-F3.3
- F5.1-F5.5

Tasks:
- M2.T1 Create engine module structure.
- M2.T2 Implement slot registry CRUD logic.
- M2.T3 Implement JSON import/export.
- M2.T4 Implement YAML import/export.
- M2.T5 Implement parent slot inheritance.
- M2.T6 Implement same-key child override.
- M2.T7 Implement deterministic condition evaluator.
- M2.T8 Implement priority-based conflict resolution.
- M2.T9 Implement prompt renderer.
- M2.T10 Implement span metadata generation.
- M2.T11 Implement missing-slot validator.
- M2.T12 Implement semantic conflict validator.
- M2.T13 Implement over-generation validator.
- M2.T14 Implement ambiguity validator.
- M2.T15 Implement rendered-vs-source fidelity validator.
- M2.T16 Add resolver, renderer, and validator unit tests.
- M2.T17 Add one end-to-end engine scenario fixture.

Exit criteria:
- Unit tests cover resolver, renderer, and validator.
- A sample `PromptSpec` can resolve, render, and validate deterministically.

## M3 Test Harness

Goal: make prompt behavior testable before UI/API complexity grows.

Covers:
- F6.1-F6.4
- F9.2
- F9.5

Tasks:
- M3.T1 Define prompt test case schema.
- M3.T2 Add fixture directory layout.
- M3.T3 Implement test case loader.
- M3.T4 Implement unit suite runner.
- M3.T5 Implement integration suite runner.
- M3.T6 Implement scenario suite runner.
- M3.T7 Implement regression suite runner.
- M3.T8 Implement expected-vs-actual meaning comparator.
- M3.T9 Implement `TestReport` writer.
- M3.T10 Add `python harness.py run` CLI.
- M3.T11 Add `python harness.py report` CLI.
- M3.T12 Add failing-test report behavior.
- M3.T13 Add harness tests with pass and fail fixtures.

Exit criteria:
- Harness can run at least one scenario test end to end.
- Failed tests produce useful report artifacts.

## M4 FastAPI Backend

Goal: expose the engine and harness through stable HTTP contracts.

Covers:
- F8.2
- API support for F1-F6

Tasks:
- M4.T1 Create FastAPI service structure.
- M4.T2 Add app configuration model.
- M4.T3 Add SQLite persistence setup.
- M4.T4 Implement `/api/prompts/resolve`.
- M4.T5 Implement `/api/prompts/render`.
- M4.T6 Implement `/api/prompts/inspect`.
- M4.T7 Implement `/api/prompts/validate`.
- M4.T8 Implement `/api/tests/run`.
- M4.T9 Implement `/api/tests/report/{report_id}`.
- M4.T10 Implement `/api/settings` GET.
- M4.T11 Implement `/api/settings` PUT.
- M4.T12 Implement `/api/ralph/status`.
- M4.T13 Implement `/api/ralph/check`.
- M4.T14 Add shared error response handling.
- M4.T15 Add API integration tests with `httpx`.

Exit criteria:
- API integration tests pass with `httpx`.
- API request/response shapes match `API_Specification.md`.

## M5 Local LLM Meaning Inspector

Goal: add optional LLM interpretation while keeping validation deterministic.

Covers:
- F4.1-F4.3
- F5.5
- Non-functional: deterministic validation first, LLM as support

Tasks:
- M5.T1 Add configurable Ollama-compatible client.
- M5.T2 Define schema-bound inspection prompt.
- M5.T3 Implement local LLM request/response handling.
- M5.T4 Implement JSON extraction and validation.
- M5.T5 Map valid output into `MeaningReport`.
- M5.T6 Map invalid/free-form output into schema failure.
- M5.T7 Store raw model output in trace logs.
- M5.T8 Add mocked LLM tests.
- M5.T9 Add one local-manual smoke test script.

Exit criteria:
- Inspector returns valid `MeaningReport`.
- Invalid/free-form model output is handled as schema failure, not accepted silently.

## M6 Web UI Prompt Studio

Goal: provide the primary user workflow.

Covers:
- F1.1-F1.3
- F3.3
- F5.1-F5.5

Tasks:
- M6.T1 Create Next.js app structure.
- M6.T2 Add design system dependencies and layout shell.
- M6.T3 Implement API client.
- M6.T4 Implement slot table.
- M6.T5 Implement slot create/edit/delete flow.
- M6.T6 Implement JSON/YAML import/export UI.
- M6.T7 Implement rendered prompt pane.
- M6.T8 Implement span highlighting and slot-to-text tracing.
- M6.T9 Implement validation report panel.
- M6.T10 Implement settings screen.
- M6.T11 Add loading, empty, and error states.
- M6.T12 Add Playwright smoke test.

Exit criteria:
- User can create slots, render a prompt, inspect spans, and see validation results in browser.
- Playwright smoke test passes.

## M7 Test Lab and Agent Trace UI

Goal: expose testing and agent observability.

Covers:
- F6.1-F6.4
- F7.1-F7.3

Tasks:
- M7.T1 Implement Test Lab screen.
- M7.T2 Implement test case list.
- M7.T3 Implement suite selector.
- M7.T4 Implement test run trigger.
- M7.T5 Implement test report viewer.
- M7.T6 Implement failure detail view.
- M7.T7 Implement Agent Trace screen.
- M7.T8 Implement trace list.
- M7.T9 Implement trace detail view.
- M7.T10 Link inspection runs to trace records.
- M7.T11 Add Playwright tests for Test Lab and Agent Trace.

Exit criteria:
- User can run a prompt test from UI and inspect pass/fail evidence.
- Agent/LLM trace is visible for inspection runs.

## M8 Ralph Loop Integration

Goal: make the repository self-driving through task-based iteration.

Covers:
- F9.1-F9.6

Tasks:
- M8.T1 Define `ralph/task_list.json` generator input rules.
- M8.T2 Implement task generator from SRS requirement IDs.
- M8.T3 Create initial `ralph/task_list.json`.
- M8.T4 Create `ralph/progress.txt`.
- M8.T5 Create `ralph/acceptance_gate.md`.
- M8.T6 Create `ralph/iteration_log.md`.
- M8.T7 Implement task selector.
- M8.T8 Implement dependency validation.
- M8.T9 Implement required test command validation.
- M8.T10 Implement `ralph-check` CLI.
- M8.T11 Implement acceptance evidence writer.
- M8.T12 Implement failure report writer.
- M8.T13 Implement `/api/ralph/status` backing logic.
- M8.T14 Implement Ralph Dashboard.
- M8.T15 Add Ralph workflow tests.

Exit criteria:
- One Ralph task can be selected, checked, tested, marked complete, and recorded with acceptance evidence.
- Failed iteration writes a failure report.

## M9 Desktop Packaging

Goal: satisfy local desktop compatibility.

Covers:
- F8.1-F8.3

Tasks:
- M9.T1 Create Tauri desktop app structure.
- M9.T2 Configure embedded web build.
- M9.T3 Configure local API connection.
- M9.T4 Add desktop startup checks.
- M9.T5 Add local storage path handling.
- M9.T6 Add desktop settings bridge.
- M9.T7 Package local development build.
- M9.T8 Add desktop smoke test checklist.
- M9.T9 Document desktop run/build commands.

Exit criteria:
- App runs as desktop shell against local backend.
- Same frontend works in web and desktop modes.

## M10 Quality Gate and Release Readiness

Goal: enforce SRS-level completeness.

Covers:
- All F1-F9
- Non-functional requirements

Tasks:
- M10.T1 Create requirement traceability matrix.
- M10.T2 Map every SRS requirement to implementation tasks.
- M10.T3 Map every SRS requirement to tests.
- M10.T4 Implement quality metrics aggregation.
- M10.T5 Implement slot coverage metric.
- M10.T6 Implement render fidelity metric.
- M10.T7 Implement conflict and ambiguity count metrics.
- M10.T8 Implement over-generation count metric.
- M10.T9 Add prompt version diff export.
- M10.T10 Add report export.
- M10.T11 Add CI workflow.
- M10.T12 Add full regression suite command.
- M10.T13 Add release checklist.
- M10.T14 Run final SRS compliance review.
- M10.T15 Fix any uncovered requirement or failing quality gate.

Exit criteria:
- Required tests pass.
- Quality gate passes.
- SRS requirement traceability matrix shows every requirement covered by implementation and tests.
