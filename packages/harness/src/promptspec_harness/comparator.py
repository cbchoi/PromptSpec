"""Expected-vs-actual meaning comparison."""

from __future__ import annotations

from typing import Any

from promptspec_harness.models import MeaningComparison


def compare_meaning(
    expected: dict[str, Any] | None,
    actual: dict[str, Any] | None,
) -> MeaningComparison:
    if expected is None:
        return MeaningComparison(status="pass")
    if actual is None:
        return MeaningComparison(status="fail", missing_keys=sorted(expected))

    missing_keys: list[str] = []
    mismatched_keys: list[str] = []
    for key, expected_value in expected.items():
        if key not in actual:
            missing_keys.append(key)
        elif actual[key] != expected_value:
            mismatched_keys.append(key)

    return MeaningComparison(
        status="fail" if missing_keys or mismatched_keys else "pass",
        missing_keys=missing_keys,
        mismatched_keys=mismatched_keys,
    )
