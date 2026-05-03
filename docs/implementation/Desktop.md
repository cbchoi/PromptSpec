# Desktop Packaging

The desktop shell is configured under `apps/desktop` using Tauri.

## Commands

```bash
corepack pnpm install
corepack pnpm --filter promptspec-desktop check
corepack pnpm --filter promptspec-desktop dev
corepack pnpm --filter promptspec-desktop build
```

## Runtime Connections

- Web frontend: shared Next.js app in `apps/web`
- API endpoint default: `http://localhost:8000`
- Local storage default: `.promptspec/app.sqlite`
- Local LLM endpoint remains configured from the web settings screen

## Smoke Checklist

- Rust and Cargo are installed.
- `corepack pnpm --filter promptspec-web build` passes.
- `corepack pnpm --filter promptspec-desktop check` passes.
- `corepack pnpm --filter promptspec-desktop dev` opens the PromptSpec window.
- Prompt Studio can run against local API or local fallback.
- Settings retain the API and local LLM endpoint values.

## Current Container Limitation

The current container does not have `rustc` or `cargo`, so Tauri cannot be built
or launched here. This blocks a real `M9` tag in this environment.

