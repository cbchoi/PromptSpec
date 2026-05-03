# Ralph Task Generator Rules

Task generation must follow these rules:

- Each generated task must map to at least one SRS requirement ID.
- Each implementation task must include acceptance criteria.
- Each implementation task must include at least one test command.
- Documentation-only tasks may use a docs verification command.
- Task IDs should use milestone task IDs from `docs/milestones/README.md` when available.
- Dependencies must reference earlier task IDs.
- A task may move to `completed` only after its test commands pass and acceptance evidence is recorded.

