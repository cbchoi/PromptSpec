"""Fixture loading for prompt test cases."""

from __future__ import annotations

import json
from pathlib import Path

import yaml

from promptspec_harness.models import PromptTestCase


def load_test_case(path: Path) -> PromptTestCase:
    if path.suffix.lower() in {".yaml", ".yml"}:
        payload = yaml.safe_load(path.read_text())
    else:
        payload = json.loads(path.read_text())
    return PromptTestCase.model_validate(payload)


def load_test_cases(directory: Path) -> list[PromptTestCase]:
    if not directory.exists():
        return []
    paths = sorted(
        path
        for path in directory.iterdir()
        if path.is_file() and path.suffix.lower() in {".json", ".yaml", ".yml"}
    )
    return [load_test_case(path) for path in paths]

