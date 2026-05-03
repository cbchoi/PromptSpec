import pytest
from promptspec_model import PromptSlot
from pydantic import ValidationError


def test_prompt_slot_accepts_canonical_fields() -> None:
    slot = PromptSlot(
        key="audience",
        type="role",
        value="Write for senior backend engineers.",
        condition=None,
        priority=100,
        source="user",
        version=1,
        required=True,
    )

    assert slot.key == "audience"
    assert slot.type == "role"
    assert slot.value == "Write for senior backend engineers."
    assert slot.condition is None
    assert slot.priority == 100
    assert slot.source == "user"
    assert slot.version == 1
    assert slot.required is True


def test_prompt_slot_defaults_match_contract() -> None:
    slot = PromptSlot(key="task", type="task", value="Summarize the document.")

    assert slot.condition is None
    assert slot.priority == 100
    assert slot.source == "user"
    assert slot.version == 1
    assert slot.required is True


@pytest.mark.parametrize("slot_type", ["unknown", "ROLE", ""])
def test_prompt_slot_rejects_invalid_type(slot_type: str) -> None:
    with pytest.raises(ValidationError):
        PromptSlot(key="audience", type=slot_type, value="x")


@pytest.mark.parametrize("source", ["unknown", "USER", ""])
def test_prompt_slot_rejects_invalid_source(source: str) -> None:
    with pytest.raises(ValidationError):
        PromptSlot(key="audience", type="role", value="x", source=source)


def test_prompt_slot_rejects_empty_key() -> None:
    with pytest.raises(ValidationError):
        PromptSlot(key="", type="role", value="x")

