# Ralph Iteration Log

## M1 Core Contracts

- Implemented canonical Pydantic models for PromptSlot, PromptSpec, RenderedPrompt, MeaningReport, ValidationReport, TestReport, and RalphTask.
- Added JSON schema export for all canonical models.
- Added unit tests for required fields, enum validation, defaults, and invalid payloads.
- Verification passed:
  - `.venv/bin/python -m pytest tests/unit`
  - `.venv/bin/ruff check .`
  - `.venv/bin/mypy`
