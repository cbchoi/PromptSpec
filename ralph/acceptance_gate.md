# Ralph Acceptance Gate

No implementation task has passed acceptance yet.

## Evidence Log

| Task | Status | Evidence | Commit |
|---|---|---|---|
| M1.T1 | pass | `.venv/bin/python -m pytest tests/unit`; `.venv/bin/ruff check .`; `.venv/bin/mypy` | M1 tag |
| M1.T2 | pass | `.venv/bin/python -m pytest tests/unit/test_prompt_slot.py`; included in full unit suite | M1 tag |
| M1.T3 | pass | `.venv/bin/python -m pytest tests/unit/test_prompt_spec.py`; included in full unit suite | M1 tag |
| M1.T4 | pass | `.venv/bin/python -m pytest tests/unit/test_rendered_prompt.py`; included in full unit suite | M1 tag |
| M1.T5 | pass | `.venv/bin/python -m pytest tests/unit/test_meaning_report.py`; included in full unit suite | M1 tag |
| M1.T6 | pass | `.venv/bin/python -m pytest tests/unit/test_validation_report.py`; included in full unit suite | M1 tag |
| M1.T7 | pass | `.venv/bin/python -m pytest tests/unit/test_test_report.py`; included in full unit suite | M1 tag |
| M1.T8 | pass | `.venv/bin/python -m pytest tests/unit/test_ralph_task.py`; included in full unit suite | M1 tag |
| M1.T9 | pass | `.venv/bin/python -m pytest tests/unit/test_schema_export.py`; included in full unit suite | M1 tag |
| M1.T10 | pass | `.venv/bin/python -m pytest tests/unit` passed 34 tests | M1 tag |
| M2.T1-M2.T17 | pass | `.venv/bin/python -m pytest tests/unit tests/scenario` passed 56 tests; `.venv/bin/ruff check .`; `.venv/bin/mypy` | M2 tag |
| M3.T1-M3.T13 | pass | `.venv/bin/python -m pytest tests/unit tests/scenario` passed 61 tests; `.venv/bin/python harness.py run --suite scenario --reports-dir /tmp/promptspec-reports`; `.venv/bin/ruff check .`; `.venv/bin/mypy` | M3 tag |
| M4.T1-M4.T15 | pass | `.venv/bin/python -m pytest tests/unit tests/scenario tests/integration` passed 66 tests; `.venv/bin/ruff check .`; `.venv/bin/mypy` | M4 tag |
| M5.T1-M5.T9 | pass | `.venv/bin/python -m pytest tests/unit tests/scenario tests/integration` passed 71 tests; `.venv/bin/ruff check .`; `.venv/bin/mypy` | M5 tag |
| M8.T1-M8.T15 | pass | `.venv/bin/python ralph_check.py M1.T1`; `.venv/bin/python -m pytest tests/unit tests/scenario tests/integration` passed 75 tests; `corepack pnpm --filter promptspec-web build`; `.venv/bin/ruff check .`; `.venv/bin/mypy` | M8 tag |
| M10.T1-M10.T14 | temp-pass | `.venv/bin/python quality_gate.py --allow-blockers`; `.venv/bin/python -m pytest tests/unit tests/scenario tests/integration` passed 79 tests; `corepack pnpm --filter promptspec-web build`; `.venv/bin/ruff check .`; `.venv/bin/mypy` | M10-temp tag |
