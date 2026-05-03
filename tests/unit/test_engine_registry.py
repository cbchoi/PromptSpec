import pytest
from promptspec_engine import SlotRegistry
from promptspec_model import PromptSlot


def slot(key: str, value: str = "value") -> PromptSlot:
    return PromptSlot(key=key, type="context", value=value)


def test_slot_registry_add_get_update_delete() -> None:
    registry = SlotRegistry()
    registry.add(slot("audience", "engineers"))

    assert registry.get("audience").value == "engineers"

    registry.update(slot("audience", "researchers"))
    assert registry.get("audience").value == "researchers"

    deleted = registry.delete("audience")
    assert deleted.value == "researchers"
    assert registry.list() == []


def test_slot_registry_rejects_duplicate_add() -> None:
    registry = SlotRegistry([slot("audience")])

    with pytest.raises(ValueError):
        registry.add(slot("audience"))


def test_slot_registry_raises_for_missing_key() -> None:
    registry = SlotRegistry()

    with pytest.raises(KeyError):
        registry.get("missing")

