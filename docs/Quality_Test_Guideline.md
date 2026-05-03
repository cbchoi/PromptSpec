# Quality Test Guideline

## Metrics
- Slot Coverage
- Render Fidelity
- Meaning Fidelity
- Conflict Count
- Ambiguity Count
- Over-Generation Count
- Ralph Task Completion Rate
- Ralph Regression Failure Rate

## Quality Gate
```text
slot_coverage = 100%
conflict_count = 0
critical_over_generation = 0
meaning_schema_valid = true
required_tests_pass = true
```

## Ralph-Specific Quality Rules
- Task cannot be completed without passing tests.
- Agent cannot edit unrelated files without explanation.
- Agent must preserve public API unless task requires change.
- Every failed iteration must produce failure report.
- Every passed iteration must record acceptance evidence.
- Every completed task must update progress.txt.

## Failure Categories
- MISSING_SLOT
- RENDER_OMISSION
- SEMANTIC_CONFLICT
- OVER_GENERATION
- AMBIGUOUS_OUTPUT
- SCHEMA_VIOLATION
- STRATEGY_MISMATCH
- RALPH_TASK_DRIFT
- RALPH_UNTESTED_COMPLETION
- RALPH_CONTEXT_LEAK
