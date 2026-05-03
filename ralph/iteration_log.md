# Ralph Iteration Log

## M1 Core Contracts

- Implemented canonical Pydantic models for PromptSlot, PromptSpec, RenderedPrompt, MeaningReport, ValidationReport, TestReport, and RalphTask.
- Added JSON schema export for all canonical models.
- Added unit tests for required fields, enum validation, defaults, and invalid payloads.
- Verification passed:
  - `.venv/bin/python -m pytest tests/unit`
  - `.venv/bin/ruff check .`
  - `.venv/bin/mypy`

## M2 Prompt Engine MVP

- Implemented slot registry CRUD logic.
- Implemented JSON/YAML slot import and export.
- Implemented deterministic condition evaluation.
- Implemented PromptSpec resolution with parent inheritance, child override, and priority handling.
- Implemented prompt rendering with exact span metadata.
- Implemented deterministic validation for missing slots, declared conflicts, over-generation, ambiguity, and span/source fidelity.
- Added unit tests and an end-to-end scenario test.
- Verification passed:
  - `.venv/bin/python -m pytest tests/unit tests/scenario`
  - `.venv/bin/ruff check .`
  - `.venv/bin/mypy`

## M3 Test Harness

- Implemented PromptTestCase schema and fixture loading.
- Implemented meaning comparison.
- Implemented HarnessRunner for suite and case execution.
- Implemented TestReport writing and loading.
- Added `harness.py run` and `harness.py report` CLI commands.
- Added pass and failure-report tests.
- Verification passed:
  - `.venv/bin/python -m pytest tests/unit tests/scenario`
  - `.venv/bin/python harness.py run --suite scenario --reports-dir /tmp/promptspec-reports`
  - `.venv/bin/ruff check .`
  - `.venv/bin/mypy`

## M4 FastAPI Backend

- Implemented FastAPI app factory and service package.
- Added SQLite-backed settings repository.
- Implemented prompt resolve, render, inspect, and validate endpoints.
- Implemented test run and test report endpoints.
- Implemented settings GET/PUT endpoints.
- Implemented Ralph status and check endpoints.
- Added shared API error response helpers.
- Added httpx integration tests.
- Verification passed:
  - `.venv/bin/python -m pytest tests/unit tests/scenario tests/integration`
  - `.venv/bin/ruff check .`
  - `.venv/bin/mypy`

## M5 Local LLM Meaning Inspector

- Implemented Ollama-compatible local LLM client.
- Implemented schema-bound inspection prompt.
- Implemented raw model JSON extraction and validation.
- Mapped valid output into MeaningReport.
- Mapped invalid/free-form output into SCHEMA_VIOLATION uncertainty.
- Added trace logging with prompt, rendered prompt, raw model output, and MeaningReport.
- Added mocked LLM tests and manual smoke script.
- Verification passed:
  - `.venv/bin/python -m pytest tests/unit tests/scenario tests/integration`
  - `.venv/bin/ruff check .`
  - `.venv/bin/mypy`

## M6 Temporary Checkpoint

- Implemented the Next.js Prompt Studio UI.
- Verified typecheck, lint, production build, and backend checks.
- Playwright smoke test is blocked because Chromium cannot launch without
  `libglib-2.0.so.0`.
- Runtime package installation is not available in the current container, so
  this state is tagged as `M6-temp` rather than `M6`.

## M7 Temporary Checkpoint

- Implemented Test Lab view with suite selector, test run trigger, test case list,
  report list, report detail, and failure-report surface.
- Implemented Agent Trace view with trace list and detailed prompt/raw/meaning view.
- Added Playwright tests for Test Lab and Agent Trace.
- Verified typecheck, lint, production build, and backend checks.
- Playwright remains blocked by missing `libglib-2.0.so.0`, so this state is
  tagged as `M7-temp` rather than `M7`.

## M8 Ralph Loop Integration

- Added Ralph task generator rules.
- Implemented Ralph task generation, loading, writing, selection, contract check,
  acceptance evidence, and failure report helpers.
- Added `ralph_check.py` CLI.
- Updated Ralph API status/check backing logic to use Ralph helpers.
- Added Ralph Dashboard in the web UI.
- Added Ralph workflow unit and integration tests.
- Verification passed:
  - `.venv/bin/python ralph_check.py M1.T1`
  - `.venv/bin/python -m pytest tests/unit tests/scenario tests/integration`
  - `corepack pnpm --filter promptspec-web typecheck`
  - `corepack pnpm --filter promptspec-web lint`
  - `corepack pnpm --filter promptspec-web build`
  - `.venv/bin/ruff check .`
  - `.venv/bin/mypy`

## M9 Temporary Checkpoint

- Added Tauri desktop app structure.
- Configured desktop shell to use the shared Next.js frontend.
- Added desktop startup/default endpoint commands.
- Added desktop environment check script and smoke checklist.
- Verified web build and backend checks.
- Tauri build is blocked because `rustc` and `cargo` are not installed, so this
  state is tagged as `M9-temp` rather than `M9`.

## M10 Temporary Checkpoint

- Added quality metrics and quality gate evaluator.
- Added quality report export and prompt version diff helper.
- Added quality gate CLI.
- Added CI workflow for backend and web static/build checks.
- Added release checklist and M10 temporary checkpoint documentation.
- Final release gate remains blocked until M6, M7, and M9 can be completed.
