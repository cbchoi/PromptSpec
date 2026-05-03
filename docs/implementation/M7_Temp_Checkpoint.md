# M7 Temporary Checkpoint

This checkpoint records the current Test Lab and Agent Trace UI implementation.
It is tagged as `M7-temp`, not `M7`, because Playwright cannot launch Chromium
in the current container.

## Implemented

- Main view tabs for Prompt Studio, Test Lab, and Agent Trace.
- Test Lab screen.
- Test case list.
- Suite selector.
- Test run trigger.
- Test report list.
- Test report detail view.
- Failure-report display surface through report detail.
- Agent Trace screen.
- Trace list.
- Trace detail view with prompt, raw model output, meaning, and uncertainty counts.
- Playwright tests for Test Lab and Agent Trace.

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

Do not create the `M7` tag until Playwright passes in an environment with the
required Chromium system dependencies installed.

