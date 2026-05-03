# Multi-Agent Specification

## Agents
- Planner Agent
- Builder Agent
- Resolver Agent
- Renderer Agent
- Inspector Agent
- Validator Agent
- Evaluator Agent
- Ralph Orchestrator Agent

## Orchestration

```text
Planner → Builder → Resolver → Renderer → Inspector → Validator → Evaluator
```

## Ralph Development Orchestration

```text
Ralph Orchestrator
  → select task
  → invoke coding agent
  → run harness
  → inspect result
  → record acceptance evidence
  → update progress
  → request commit
```

## Output Contract
All agents return JSON only unless the task explicitly requires Markdown documentation.
Machine-facing payloads must use the contracts in `Data_Model.md`.
No free-form prose in machine-facing outputs.

## Ralph Orchestrator Responsibilities
- read task_list.json
- select exactly one incomplete task
- verify prerequisite tasks
- execute implementation plan
- run test commands
- record acceptance evidence in ralph/acceptance_gate.md
- update progress.txt
- create iteration report
- mark task complete only after acceptance gate passes
