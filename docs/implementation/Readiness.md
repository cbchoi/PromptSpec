# Implementation Readiness

This document records the project decisions required before implementation.

## Tooling Decisions

- Python runtime: Python 3.11+
- Python package tooling: `uv` or standard `pip` with `pyproject.toml`
- Backend framework: FastAPI
- Data contracts: Pydantic v2
- Persistence: SQLite through SQLModel
- Backend tests: pytest
- Backend HTTP tests: pytest + httpx
- Static checks: ruff and mypy
- Frontend package manager: pnpm
- Frontend framework: Next.js + React + TypeScript
- Desktop shell: Tauri
- E2E tests: Playwright

## Initial Commands

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
ruff check .
mypy
```

Frontend commands will become active after the Next.js app is created:

```bash
pnpm install
pnpm lint
pnpm typecheck
pnpm test
```

## Implementation Entry Point

Start with milestone `M1 Core Contracts`.

First task:

```text
M1.T1 Define package layout for shared model code.
```

The current scaffold already creates the intended package and test directories.
The next implementation step should add tests and Pydantic models under
`packages/model/src/promptspec_model/`.

## Readiness Checklist

- [x] SRS has stable requirement IDs.
- [x] Canonical data model exists in `docs/Data_Model.md`.
- [x] Milestone task plan exists in `docs/milestones/README.md`.
- [x] Requirement traceability matrix exists.
- [x] Ralph task list exists.
- [x] Ralph progress and acceptance files exist.
- [x] Root tooling config exists.
- [x] Initial package/test directories exist.
- [ ] M1 implementation code exists.
- [ ] M1 tests pass.

