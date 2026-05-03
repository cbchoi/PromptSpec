# Ralph Loop Specification

## 1. Purpose
Ralph Loop는 AI coding agent가 동일한 high-level instruction을 반복 실행하되, 각 iteration은 fresh context로 시작하고 상태는 파일과 git history에 남기는 개발 방식이다.

## 2. Core Principle
- fresh context per iteration
- persistent state in files
- one task per iteration
- test-first or test-gated development
- commit after passing acceptance
- no completion without validation

## 3. Required Files

```text
ralph/
  task_list.json
  progress.txt
  loop_prompt.md
  acceptance_gate.md
  iteration_log.md

reports/
  ralph/
```

## 4. task_list.json Schema

```json
{
  "tasks": [
    {
      "id": "T001",
      "title": "Implement PromptSlot model",
      "status": "pending",
      "source_doc": "SRS.md",
      "acceptance_criteria": [
        "PromptSlot has key/type/value/condition/priority/source/version"
      ],
      "test_commands": [
        "pytest tests/unit/test_prompt_slot.py"
      ],
      "dependencies": []
    }
  ]
}
```

This schema is also defined as `RalphTask` in `Data_Model.md`.

## 5. progress.txt Format

```text
Completed:
- T001 Implement PromptSlot model

In Progress:
- T002 Implement slot resolver

Blocked:
- None

Last Failure:
- None
```

## 6. Iteration Algorithm

```text
while incomplete tasks exist:
    load task_list.json
    load progress.txt
    select one task
    implement minimal change
    run tests
    if tests pass:
        record acceptance evidence
        mark complete
        update progress
        commit
    else:
        write reports/ralph/failure_<task_id>.md
        stop or retry depending on policy
```

## 7. Stop Conditions
- all tasks complete
- test failure unresolved
- missing requirement
- unsafe file operation
- repeated failure over retry limit
