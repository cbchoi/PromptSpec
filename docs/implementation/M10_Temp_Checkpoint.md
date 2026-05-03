# M10 Temporary Checkpoint

This checkpoint records the current quality gate and release readiness state. It
is tagged as `M10-temp`, not `M10`, because release blockers remain unresolved.

## Implemented

- Requirement traceability matrix exists.
- Quality metrics model.
- Quality gate evaluator.
- Quality report export.
- Prompt version diff helper.
- Quality gate CLI.
- CI workflow document for backend and web static/build checks.
- Release checklist.

## Verified

```bash
.venv/bin/python -m pytest tests/unit tests/scenario tests/integration
.venv/bin/ruff check .
.venv/bin/mypy
corepack pnpm --filter promptspec-web typecheck
corepack pnpm --filter promptspec-web lint
corepack pnpm --filter promptspec-web build
.venv/bin/python quality_gate.py --allow-blockers
```

## Blocked

The final quality gate intentionally fails without `--allow-blockers` because
these release blockers remain:

- `M6` is not complete.
- `M7` is not complete.
- `M9` is not complete.
