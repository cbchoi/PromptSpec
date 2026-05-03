from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
for source_path in ("packages/model/src", "packages/engine/src", "packages/harness/src"):
    sys.path.insert(0, str(ROOT / source_path))


def main() -> int:
    from promptspec_harness.reporting import load_test_report
    from promptspec_harness.runner import HarnessRunner

    parser = argparse.ArgumentParser(prog="harness.py")
    subparsers = parser.add_subparsers(dest="command", required=True)

    run_parser = subparsers.add_parser("run")
    run_parser.add_argument("--suite", default="scenario")
    run_parser.add_argument("--fixtures-dir", default="fixtures")
    run_parser.add_argument("--reports-dir", default="reports/tests")

    report_parser = subparsers.add_parser("report")
    report_parser.add_argument("report_id")
    report_parser.add_argument("--reports-dir", default="reports/tests")

    args = parser.parse_args()

    if args.command == "run":
        runner = HarnessRunner(Path(args.fixtures_dir), Path(args.reports_dir))
        report = runner.run_suite(args.suite)
        print(report.model_dump_json(indent=2))
        return 0 if report.status == "pass" else 1

    report = load_test_report(args.report_id, Path(args.reports_dir))
    print(report.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
