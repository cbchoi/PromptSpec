# SDD - Software Design Document

## 1. Architecture

```text
Next.js UI
   ↓
FastAPI Backend
   ↓
Prompt Engine
   ├─ Slot Registry
   ├─ Slot Resolver
   ├─ Policy Engine
   ├─ Renderer
   └─ Validator

Agent Layer
   └─ Meaning Inspector

Harness
   └─ Test Runner / Ralph Gate

Storage
   └─ SQLite / JSON / YAML

Agent Layer → Local LLM endpoint
```

## 2. Ralph Loop Architecture

```text
docs/
  SRS.md
  SDD.md
  UI_Design.md
  API_Specification.md
  Acceptance_Test_Prompt.md

ralph/
  task_list.json
  progress.txt
  loop_prompt.md
  iteration_log.md
  acceptance_gate.md

reports/
  ralph/
  tests/
```

## 3. Deployment Modes

### Web Mode
```text
Browser → Next.js → FastAPI → SQLite/LLM
```

### Local Desktop Mode
```text
Tauri App → embedded Next.js frontend → local FastAPI → SQLite/Ollama
```

## 4. Frontend
- Next.js App Router
- React
- TypeScript
- Tailwind CSS
- shadcn/ui
- TanStack Table
- React Flow or Mermaid renderer
- Monaco Editor

## 5. Backend
- FastAPI
- Pydantic models
- SQLite via SQLModel or SQLAlchemy
- pytest-based harness
- HTTP API for prompt operations

## 6. Prompt Composition
상속은 class inheritance가 아니라 slot inheritance로 구현한다.

```text
parent slots + child slots
→ merge
→ override
→ condition resolve
→ PromptSpec
```

## 7. Polymorphism
다형성은 strategy slot으로 구현한다.

```json
{
  "render_strategy": "technical_report",
  "validation_strategy": "strict_source_based",
  "inspection_strategy": "schema_bound_local_llm"
}
```

## 8. Ralph Loop State Model

Ralph Loop에서는 agent memory에 의존하지 않는다.

Persistent state:
- task_list.json
- progress.txt
- acceptance_gate.md
- iteration_log.md
- git history
- failing test reports
- acceptance reports
- implementation notes

Each iteration:
1. Load task_list.json
2. Load progress.txt
3. Select one incomplete task
4. Implement minimum change
5. Run specified tests
6. If pass, record acceptance evidence, update progress, and commit
7. If fail, write failure report
8. End iteration

## 9. Data Contracts

`Data_Model.md` is the canonical contract for `PromptSlot`, `PromptSpec`,
`RenderedPrompt`, `MeaningReport`, `ValidationReport`, `TestReport`, and
`RalphTask`. Other documents may add behavior, but must not redefine fields.

## 10. Structure Reflection

## Separation of Concerns

| Layer | Responsibility |
|------|----------------|
| model | data definition |
| engine | deterministic logic |
| agents | LLM interaction |
| harness | testing / validation |
| services | API |
| apps | UI |

## Execution Flow

```text
UI (Next.js)
→ API (FastAPI)
→ Engine
→ Model
→ Agents (optional meaning inspection)
→ Validation
→ Response
```

## Prompt Pipeline

```text
Slots (model)
→ Resolver (engine)
→ PromptSpec
→ Renderer (engine)
→ Rendered Prompt
→ Inspector (agent)
→ MeaningReport
→ Validator (engine)
```
