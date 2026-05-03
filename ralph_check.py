from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for source_path in (
    "packages/model/src",
    "packages/engine/src",
    "packages/harness/src",
):
    sys.path.insert(0, str(ROOT / source_path))


def main() -> int:
    from promptspec_harness import load_tasks, validate_task_contract

    parser = argparse.ArgumentParser(prog="ralph_check.py")
    parser.add_argument("task_id")
    parser.add_argument("--task-list", default="ralph/task_list.json")
    args = parser.parse_args()

    tasks = load_tasks(Path(args.task_list))
    task = next((item for item in tasks if item.id == args.task_id), None)
    if task is None:
        print(f"Task not found: {args.task_id}", file=sys.stderr)
        return 1

    report = validate_task_contract(task)
    print(report.model_dump_json(indent=2))
    return 0 if report.status == "pass" else 1


if __name__ == "__main__":
    raise SystemExit(main())
