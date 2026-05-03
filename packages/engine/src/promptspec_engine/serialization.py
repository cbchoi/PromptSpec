"""JSON and YAML import/export helpers for prompt slots."""

from __future__ import annotations

import json

import yaml
from promptspec_model import PromptSlot


def slots_to_json(slots: list[PromptSlot]) -> str:
    return json.dumps([slot.model_dump() for slot in slots], indent=2)


def slots_from_json(payload: str) -> list[PromptSlot]:
    loaded = json.loads(payload)
    if not isinstance(loaded, list):
        raise ValueError("slot JSON payload must be a list")
    return [PromptSlot.model_validate(item) for item in loaded]


def slots_to_yaml(slots: list[PromptSlot]) -> str:
    return yaml.safe_dump([slot.model_dump() for slot in slots], sort_keys=False)


def slots_from_yaml(payload: str) -> list[PromptSlot]:
    loaded = yaml.safe_load(payload)
    if not isinstance(loaded, list):
        raise ValueError("slot YAML payload must be a list")
    return [PromptSlot.model_validate(item) for item in loaded]
