"""Deterministic condition evaluation for prompt slots."""

from __future__ import annotations

import re
from typing import Any

_COMPARISON_RE = re.compile(r"^\s*([A-Za-z_][A-Za-z0-9_]*)\s*(==|!=)\s*(.+?)\s*$")


def evaluate_condition(condition: str | None, context: dict[str, Any]) -> bool:
    """Evaluate a small deterministic condition language.

    Supported forms:
    - `None` or empty string: active
    - `flag`: truthiness of `context["flag"]`
    - `not flag` or `!flag`: inverse truthiness
    - `name == value`
    - `name != value`
    """

    if condition is None or condition.strip() == "":
        return True

    expression = condition.strip()
    if expression.startswith("not "):
        return not bool(context.get(expression[4:].strip()))
    if expression.startswith("!"):
        return not bool(context.get(expression[1:].strip()))

    comparison = _COMPARISON_RE.match(expression)
    if comparison:
        key, operator, raw_expected = comparison.groups()
        expected = _parse_literal(raw_expected)
        actual = context.get(key)
        if operator == "==":
            return bool(actual == expected)
        return bool(actual != expected)

    return bool(context.get(expression))


def _parse_literal(value: str) -> Any:
    stripped = value.strip()
    if (stripped.startswith('"') and stripped.endswith('"')) or (
        stripped.startswith("'") and stripped.endswith("'")
    ):
        return stripped[1:-1]
    lowered = stripped.lower()
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    if lowered == "null":
        return None
    try:
        return int(stripped)
    except ValueError:
        return stripped
