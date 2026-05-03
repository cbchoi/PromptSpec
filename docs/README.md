# Prompt Architecture Standalone App - Ralph Loop Edition

## Stack
- Frontend: Next.js + React + TypeScript
- Desktop Shell: Tauri
- Backend API: FastAPI
- Local LLM: Ollama or compatible local inference server
- Database: SQLite
- Test: pytest + Playwright
- Development Loop: Ralph Loop

## Source of Truth
- Product requirements: `SRS.md`
- Architecture and boundaries: `SDD.md`
- Data contracts: `Data_Model.md`
- HTTP contracts: `API_Specification.md`
- Ralph workflow: `Ralph_Loop_Specification.md`
- Milestone task plan: `milestones/README.md`
- Implementation readiness: `implementation/Readiness.md`
- Requirement traceability: `implementation/Traceability_Matrix.md`

## Goal
Build a local/web-compatible tool for slot-based prompt design, dynamic prompt composition, rendering, meaning inspection, validation, and test-driven prompt engineering.

## Core Concept

```text
Abstract Intent
→ Slot Graph
→ Resolved PromptSpec
→ Rendered Prompt
→ Meaning Inspection
→ Validation Report
```

## Ralph Loop Development Concept

```text
PRD / SRS / SDD / Test Spec
→ task_list.json
→ Ralph iteration
→ implement one task
→ run tests
→ record acceptance evidence
→ update progress
→ commit
→ fresh context
→ next task
```

The agent must not rely on chat memory.  
Persistent state must live in files, tests, reports, and git commits.
