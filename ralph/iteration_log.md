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
