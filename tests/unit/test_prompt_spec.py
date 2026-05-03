import pytest
from promptspec_model import PromptSlot, PromptSpec, PromptStrategy
from pydantic import ValidationError


def strategy() -> PromptStrategy:
    return PromptStrategy(
        render_strategy="technical_report",
        validation_strategy="strict_source_based",
        inspection_strategy="schema_bound_local_llm",
    )


def test_prompt_spec_accepts_canonical_fields() -> None:
    spec = PromptSpec(
        id="spec_001",
        title="Technical report prompt",
        parent_id=None,
        slots=[PromptSlot(key="audience", type="role", value="Senior engineers")],
        strategy=strategy(),
        metadata={"owner": "tests"},
    )

    assert spec.id == "spec_001"
    assert spec.title == "Technical report prompt"
    assert spec.parent_id is None
    assert spec.slots[0].key == "audience"
    assert spec.strategy.render_strategy == "technical_report"
    assert spec.metadata == {"owner": "tests"}


def test_prompt_spec_rejects_duplicate_slot_keys() -> None:
    with pytest.raises(ValidationError):
        PromptSpec(
            id="spec_001",
            title="Duplicate slots",
            slots=[
                PromptSlot(key="audience", type="role", value="A"),
                PromptSlot(key="audience", type="context", value="B"),
            ],
            strategy=strategy(),
        )


def test_prompt_spec_preserves_strategy_values() -> None:
    spec = PromptSpec(id="spec_001", title="Prompt", strategy=strategy())

    assert spec.strategy.model_dump() == {
        "render_strategy": "technical_report",
        "validation_strategy": "strict_source_based",
        "inspection_strategy": "schema_bound_local_llm",
    }

