# CI Workflow

The GitHub token available in this environment cannot create or update files
under `.github/workflows` because it lacks `workflow` scope. Use this document
as the CI workflow source until a properly scoped token can add the live
workflow file.

```yaml
name: CI

on:
  push:
  pull_request:

jobs:
  backend:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: python -m pip install -e ".[dev]"
      - run: python -m pytest tests/unit tests/scenario tests/integration
      - run: ruff check .
      - run: mypy

  web:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-node@v4
        with:
          node-version: "20"
      - run: corepack enable
      - run: corepack pnpm install
      - run: corepack pnpm --filter promptspec-web typecheck
      - run: corepack pnpm --filter promptspec-web lint
      - run: corepack pnpm --filter promptspec-web build
```

