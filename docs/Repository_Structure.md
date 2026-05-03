# Repository Structure (Updated)

## Root

```text
promptspec/
├─ apps/
│  ├─ web/               # Next.js frontend
│  └─ desktop/           # Tauri wrapper
│
├─ services/
│  └─ api/               # FastAPI backend
│
├─ packages/
│  ├─ model/             # Core data structures (PromptSpec, Slot)
│  ├─ engine/            # Resolver, Renderer, Validator
│  ├─ agents/            # Multi-agent logic
│  ├─ harness/           # TDD + test execution
│  └─ schema/            # JSON schema / validation rules
│
├─ ralph/                # Ralph loop state (IMPORTANT)
│  ├─ task_list.json
│  ├─ progress.txt
│  ├─ loop_prompt.md
│  ├─ acceptance_gate.md
│  └─ iteration_log.md
│
├─ tests/                # pytest tests
├─ reports/
│  ├─ tests/
│  └─ ralph/
├─ docs/                 # SRS, SDD, etc.
└─ infra/                # Docker, config
```

## Design Principles

- model: pure data (no logic)
- engine: deterministic logic
- agents: LLM-driven behavior
- harness: testing & validation
- apps: UI layer
- services: API layer

## Key Rule

```text
DO NOT mix:
- data (model)
- logic (engine)
- AI behavior (agents)
```

## Ralph Loop Constraint

```text
ralph/ must be at root level.
Do NOT move it into packages.
Failed Ralph iterations write reports to reports/ralph/.
```
