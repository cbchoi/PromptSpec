# Ralph Loop Prompt

You are operating inside a Ralph Loop for this repository.

## Objective
Build the Prompt Architecture Standalone App according to the documents in /docs and task list in /ralph/task_list.json.

## Loop Rules
1. Start with fresh context.
2. Read ralph/task_list.json and ralph/progress.txt.
3. Select exactly one incomplete task.
4. Do not work on multiple tasks in one iteration.
5. Write or update tests before implementation when applicable.
6. Implement the smallest change needed.
7. Run the task's required tests.
8. If tests pass:
   - record acceptance evidence
   - mark the task complete
   - update ralph/progress.txt
   - create a concise commit message
9. If tests fail:
   - do not mark complete
   - write reports/ralph/failure_<task_id>.md
10. Do not claim completion without evidence.

## Output
At the end of each iteration, output:

```json
{
  "task_id": "",
  "status": "completed|failed|blocked",
  "files_changed": [],
  "tests_run": [],
  "test_result": "pass|fail",
  "progress_updated": true,
  "commit_message": ""
}
```
