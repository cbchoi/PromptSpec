# M9 Temporary Checkpoint

This checkpoint records the current desktop packaging implementation state. It
is tagged as `M9-temp`, not `M9`, because Rust/Cargo are not installed in the
current container.

## Implemented

- Tauri app package under `apps/desktop`.
- Tauri configuration for shared Next.js frontend.
- Rust app entry point.
- Desktop commands for API endpoint and storage path defaults.
- Desktop environment check script.
- Desktop run/build documentation.
- Desktop smoke checklist.

## Verified

```bash
corepack pnpm --filter promptspec-web build
.venv/bin/python -m pytest tests/unit tests/scenario tests/integration
.venv/bin/ruff check .
.venv/bin/mypy
```

## Blocked

```bash
corepack pnpm --filter promptspec-desktop build
```

Reason:

```text
rustc and cargo are not installed in the current container.
```

## Completion Rule

Do not create the `M9` tag until the Tauri desktop app builds and the smoke
checklist passes in an environment with Rust/Cargo installed.

