# Agent Instructions

## Common Rules
- Do not invent missing user intent.
- Do not add fields outside the schema.
- If uncertain, mark as uncertain.
- Prefer rule-based validation over LLM judgment.
- All agent outputs must be JSON unless asked to generate documents.
- Use `Data_Model.md` for machine-facing data contracts.
- Never mark a task complete unless tests pass.

## Ralph Loop Instruction
You are running inside a Ralph Loop.

At the start of each iteration:
1. Read ralph/task_list.json.
2. Read ralph/progress.txt.
3. Select exactly one incomplete task.
4. Read only the files needed for that task.
5. Implement the smallest change that satisfies the task.
6. Run the task's required tests.
7. If tests pass, record acceptance evidence, update progress.txt, and prepare commit message.
8. If tests fail, write reports/ralph/failure_<task_id>.md and do not mark complete.
9. End the iteration.

Do not depend on previous chat context.
Persistent state must be written to files.

## Planner Instruction
Convert user requirement into required slots, optional slots, risk flags, and next actions.

## Builder Instruction
Create PromptSlot objects from Planner output.

## Resolver Instruction
Apply inheritance, merge, override, condition evaluation, and priority rules.

## Renderer Instruction
Render PromptSpec into natural language prompt and span metadata.

## Inspector Instruction
Interpret rendered prompt into fixed MeaningReport schema.

## Validator Instruction
Compare PromptSpec, RenderedPrompt, and MeaningReport.
