"""In-memory slot registry operations."""

from __future__ import annotations

from promptspec_model import PromptSlot


class SlotRegistry:
    """CRUD wrapper for prompt slots keyed by slot key."""

    def __init__(self, slots: list[PromptSlot] | None = None) -> None:
        self._slots: dict[str, PromptSlot] = {}
        for slot in slots or []:
            self.add(slot)

    def add(self, slot: PromptSlot) -> None:
        if slot.key in self._slots:
            raise ValueError(f"slot already exists: {slot.key}")
        self._slots[slot.key] = slot

    def update(self, slot: PromptSlot) -> None:
        if slot.key not in self._slots:
            raise KeyError(slot.key)
        self._slots[slot.key] = slot

    def delete(self, key: str) -> PromptSlot:
        if key not in self._slots:
            raise KeyError(key)
        return self._slots.pop(key)

    def get(self, key: str) -> PromptSlot:
        if key not in self._slots:
            raise KeyError(key)
        return self._slots[key]

    def list(self) -> list[PromptSlot]:
        return list(self._slots.values())

