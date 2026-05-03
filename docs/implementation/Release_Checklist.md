# Release Checklist

## Required Gates

- [ ] `M6` tag exists.
- [ ] `M7` tag exists.
- [ ] `M9` tag exists.
- [ ] `M10` tag exists.
- [ ] Backend unit, scenario, and integration tests pass.
- [ ] Web typecheck, lint, and build pass.
- [ ] Playwright smoke tests pass.
- [ ] Tauri desktop build passes.
- [ ] Quality gate report status is `pass`.
- [ ] Requirement traceability matrix has no uncovered SRS requirement.
- [ ] Live `.github/workflows/ci.yml` exists after pushing with a token that has `workflow` scope.

## Current Blockers

- `M6` is only tagged as `M6-temp` because Playwright cannot launch Chromium in the current container.
- `M7` is only tagged as `M7-temp` for the same Playwright dependency blocker.
- `M9` is only tagged as `M9-temp` because Rust/Cargo are unavailable in the current container.

## Release Command Set

```bash
.venv/bin/python -m pytest tests/unit tests/scenario tests/integration
.venv/bin/ruff check .
.venv/bin/mypy
corepack pnpm --filter promptspec-web typecheck
corepack pnpm --filter promptspec-web lint
corepack pnpm --filter promptspec-web build
corepack pnpm --filter promptspec-web test
corepack pnpm --filter promptspec-desktop build
.venv/bin/python quality_gate.py
```
