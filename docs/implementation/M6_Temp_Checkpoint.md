# M6 Temporary Checkpoint

This checkpoint records the current Web UI Prompt Studio implementation state.
It is tagged as `M6-temp`, not `M6`, because the Playwright browser smoke test
is blocked by container OS dependencies.

## Implemented

- Next.js web app structure under `apps/web`.
- Prompt Studio operational screen.
- Slot table.
- Slot create, edit, and delete flow.
- JSON import/export UI.
- Rendered prompt pane with slot highlighting.
- Validation panel.
- Settings inputs for API and local LLM endpoints.
- Playwright smoke test file.

## Verified

```bash
corepack pnpm --filter promptspec-web typecheck
corepack pnpm --filter promptspec-web lint
corepack pnpm --filter promptspec-web build
.venv/bin/python -m pytest tests/unit tests/scenario tests/integration
.venv/bin/ruff check .
.venv/bin/mypy
```

## Blocked

```bash
corepack pnpm --filter promptspec-web test
```

Reason:

```text
Chromium cannot launch because libglib-2.0.so.0 is missing.
The container does not permit runtime apt installs, even from a root shell.
```

## Completion Rule

Do not create the `M6` tag until Playwright passes in an environment with the
required Chromium system dependencies installed.

