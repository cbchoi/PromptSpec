# SRS - Software Requirements Specification

## 1. Purpose
이 앱은 slot 기반 prompt architecture를 실험하고 검증하기 위한 standalone tool이다.
Web과 Local Desktop 양쪽에서 동일한 기능을 제공한다.
개발 방식은 TDD와 Ralph Loop 기반 반복 개발을 전제로 한다.

## 2. Target Platform
- Web: Browser-based Next.js app
- Local Desktop: Tauri app
- Backend: FastAPI
- Local LLM: Ollama or compatible server
- Storage: SQLite
- Development loop: Ralph Loop

## 3. Users
- Prompt engineer
- LLM application developer
- AI researcher
- Multi-agent workflow designer

## 4. Functional Requirements

### F1. Slot Management
- F1.1 The app shall add, edit, and delete prompt slots.
- F1.2 Each slot shall support the canonical `PromptSlot` fields in `Data_Model.md`.
- F1.3 The app shall import and export slot sets as JSON and YAML.

### F2. Prompt Composition
- F2.1 Child prompt specs shall inherit parent slots.
- F2.2 Child slots shall override parent slots with the same key.
- F2.3 Conditional slots shall activate only when their condition evaluates true.
- F2.4 Conflicting active slots shall resolve by deterministic priority rules.

### F3. Rendering
- F3.1 The renderer shall convert a `PromptSpec` into natural language prompt text.
- F3.2 The renderer shall return `RenderedPrompt.spans` for source slot tracing.
- F3.3 The UI shall display color-coded slot-to-span mapping.

### F4. Meaning Inspection
- F4.1 The inspector shall use a configurable local LLM endpoint.
- F4.2 The inspector shall return schema-bound `MeaningReport` JSON.
- F4.3 Uncertain interpretations shall be represented in `uncertainties`.

### F5. Validation
- F5.1 Validation shall fail when required slots are missing from rendered output.
- F5.2 Validation shall detect semantic conflicts between active slots.
- F5.3 Validation shall detect over-generation not supported by source slots.
- F5.4 Validation shall detect ambiguous rendered meaning.
- F5.5 Validation shall compare rendered prompt and original slots for fidelity.

### F6. TDD Support
- F6.1 Users shall create prompt test cases.
- F6.2 The harness shall run unit, integration, scenario, regression, and UI tests.
- F6.3 The harness shall compare expected meaning and actual meaning.
- F6.4 The harness shall generate pass/fail `TestReport` artifacts.

### F7. Multi-Agent Development Support
- F7.1 Planner, Builder, Resolver, Renderer, Inspector, Validator, and Evaluator roles shall have separate responsibilities.
- F7.2 Agent input and output shall use explicit JSON schemas.
- F7.3 Agent execution traces shall be stored for inspection.

### F8. Web/Local Compatibility
- F8.1 Web and Tauri desktop shall use the same frontend application.
- F8.2 FastAPI shall run as either a local service or a remote API.
- F8.3 The local LLM endpoint shall be configurable.

### F9. Ralph Loop Development Support
- F9.1 The Ralph task generator shall create `ralph/task_list.json` from PRD/SRS/SDD inputs.
- F9.2 Each Ralph task shall include acceptance criteria and test commands.
- F9.3 Each iteration shall update `ralph/progress.txt`.
- F9.4 Failed iterations shall write reports to `reports/ralph/`.
- F9.5 Tasks shall be completed only after tests and acceptance gate pass.
- F9.6 Completed tasks shall be eligible for git commit.

## 5. Acceptance Traceability

Each implementation task must map to one or more requirement IDs above. Each
task must include at least one test command unless it is documentation-only.

## 6. Non-Functional Requirements
- deterministic validation 우선
- LLM 판단은 보조적 역할
- 모든 결과는 재현 가능해야 함
- prompt 변경 이력 추적 가능
- offline/local-first 동작 지원
- Ralph iteration은 fresh context 원칙을 따른다
