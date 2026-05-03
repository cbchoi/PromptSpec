# TDD Strategy

## Principle
```text
Write failing test
→ implement minimal feature
→ run test
→ refactor
→ regression test
```

## Ralph Integration
Every Ralph task must include:
- mapped requirement IDs
- expected behavior
- acceptance criteria
- required test file
- test command
- completion rule

A Ralph iteration is not complete until tests pass.

## Test Layers
- Unit Tests
- Integration Tests
- Scenario Tests
- Regression Tests
- UI Tests

## Acceptance Criteria
- All required slots resolved
- No unresolved conflict
- Rendered prompt contains all mandatory constraints
- Meaning report matches expected schema
- Validation report pass

## Recommended Tools
- Backend: pytest
- API: pytest + httpx
- Frontend: Playwright
- Static typing: mypy or pyright
- Lint: ruff
