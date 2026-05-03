"""Harness data structures."""

from __future__ import annotations

from typing import Any, Literal

from promptspec_model import PromptSpec, TestSuite
from pydantic import BaseModel, ConfigDict, Field

ExpectedStatus = Literal["pass", "fail"]


class PromptTestCase(BaseModel):
    """Fixture describing an end-to-end prompt test case."""

    model_config = ConfigDict(extra="forbid")

    id: str = Field(min_length=1)
    suite: TestSuite
    prompt_spec: PromptSpec
    parents: dict[str, PromptSpec] = Field(default_factory=dict)
    expected_status: ExpectedStatus = "pass"
    expected_text: str | None = None
    expected_meaning: dict[str, Any] | None = None


class MeaningComparison(BaseModel):
    """Result of comparing expected and actual meaning dictionaries."""

    model_config = ConfigDict(extra="forbid")

    status: ExpectedStatus
    missing_keys: list[str] = Field(default_factory=list)
    mismatched_keys: list[str] = Field(default_factory=list)

