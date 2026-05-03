"""Harness report writing."""

from __future__ import annotations

import json
from pathlib import Path

from promptspec_model import TestReport


def write_test_report(report: TestReport, reports_dir: Path) -> Path:
    reports_dir.mkdir(parents=True, exist_ok=True)
    path = reports_dir / f"{report.report_id}.json"
    path.write_text(json.dumps(report.model_dump(), indent=2))
    return path


def load_test_report(report_id: str, reports_dir: Path) -> TestReport:
    path = reports_dir / f"{report_id}.json"
    return TestReport.model_validate_json(path.read_text())

