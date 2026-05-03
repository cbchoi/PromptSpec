# Implementation Roadmap

## Phase 1 - Engine MVP
- PromptSlot model
- PromptSpec / RenderedPrompt / ValidationReport contracts
- Slot resolver
- Renderer
- Basic validator
- pytest unit tests

## Phase 2 - FastAPI Backend
- API routes
- SQLite persistence
- test harness endpoint

## Phase 3 - Next.js UI
- Slot table
- Rendered prompt pane
- Meaning report pane
- Validation pane

## Phase 4 - Tauri Desktop
- Package Next.js UI
- Connect to local FastAPI
- Settings for local LLM endpoint

## Phase 5 - Multi-Agent Harness
- Agent schema
- Agent trace view
- scenario tests
- regression suite

## Phase 6 - Ralph Loop Integration
- task_list.json generation
- progress.txt tracking
- acceptance_gate.md evidence recording
- ralph-check command
- Ralph dashboard
- failure reports
- completion gate

## Phase 7 - Quality Gate
- local test run
- report export
- prompt version diff
- acceptance evidence tracking
