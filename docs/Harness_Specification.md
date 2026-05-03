# Harness Specification

## Purpose
Prompt architecture engine과 Ralph Loop iteration의 품질을 자동 검증한다.

## Directory Structure

```text
tests/
  unit/
  integration/
  scenario/
  regression/
  e2e/
fixtures/
  prompts/
  contexts/
  expected/
reports/
  tests/
  ralph/
ralph/
  task_list.json
  progress.txt
  loop_prompt.md
  acceptance_gate.md
  iteration_log.md
```

## CLI

```bash
python harness.py run
python harness.py run --suite scenario
python harness.py report
python harness.py ralph-check
```

## Test Flow

```text
load testcase
→ resolve slots
→ render prompt
→ inspect meaning
→ validate
→ compare expected
→ write report
```

## Ralph Check Flow

```text
load current task
→ verify acceptance criteria exist
→ verify tests exist
→ run required tests
→ write acceptance evidence to ralph/acceptance_gate.md
→ verify progress update
→ verify no unrelated changes
→ generate ralph report
```

Failure reports are written to `reports/ralph/`. Test reports are written to
`reports/tests/`.
