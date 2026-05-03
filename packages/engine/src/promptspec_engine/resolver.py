"""PromptSpec inheritance, condition, override, and priority resolution."""

from __future__ import annotations

from collections.abc import Mapping
from typing import Any

from promptspec_model import PromptSlot, PromptSpec

from promptspec_engine.conditions import evaluate_condition


def resolve_prompt_spec(
    spec: PromptSpec,
    parents: Mapping[str, PromptSpec] | None = None,
    context: dict[str, Any] | None = None,
) -> PromptSpec:
    """Resolve a PromptSpec into active, unique slots.

    Parent slots are loaded first. Child slots override parent slots with the
    same key. For slots introduced from the same level, higher priority wins.
    Conditions are evaluated against supplied context plus `spec.metadata`.
    """

    resolution_context = {**spec.metadata, **(context or {})}
    inherited_slots: list[PromptSlot] = []
    if spec.parent_id is not None:
        if parents is None or spec.parent_id not in parents:
            raise KeyError(f"missing parent PromptSpec: {spec.parent_id}")
        parent = resolve_prompt_spec(parents[spec.parent_id], parents, resolution_context)
        inherited_slots = parent.slots

    merged = _merge_slots(inherited_slots, spec.slots)
    active_slots = [
        slot for slot in merged if evaluate_condition(slot.condition, resolution_context)
    ]
    active_slots = _resolve_priority_conflict_groups(active_slots, spec.metadata)

    return spec.model_copy(update={"slots": active_slots})


def _merge_slots(parent_slots: list[PromptSlot], child_slots: list[PromptSlot]) -> list[PromptSlot]:
    merged: dict[str, PromptSlot] = {}
    order: list[str] = []

    for slot in parent_slots:
        _merge_one(merged, order, slot, child_override=False)
    for slot in child_slots:
        _merge_one(merged, order, slot, child_override=True)

    return [merged[key] for key in order]


def _merge_one(
    merged: dict[str, PromptSlot],
    order: list[str],
    slot: PromptSlot,
    *,
    child_override: bool,
) -> None:
    if slot.key not in merged:
        merged[slot.key] = slot
        order.append(slot.key)
        return

    current = merged[slot.key]
    if child_override or slot.priority > current.priority:
        merged[slot.key] = slot


def _resolve_priority_conflict_groups(
    slots: list[PromptSlot],
    metadata: dict[str, Any],
) -> list[PromptSlot]:
    groups = metadata.get("conflict_groups", [])
    if not isinstance(groups, list):
        return slots

    keep_keys = {slot.key for slot in slots}
    slots_by_key = {slot.key: slot for slot in slots}
    for group in groups:
        if not isinstance(group, list):
            continue
        active_group = [slots_by_key[key] for key in group if key in slots_by_key]
        if len(active_group) < 2:
            continue
        winner = max(active_group, key=lambda slot: slot.priority)
        for slot in active_group:
            if slot.key != winner.key:
                keep_keys.discard(slot.key)

    return [slot for slot in slots if slot.key in keep_keys]
