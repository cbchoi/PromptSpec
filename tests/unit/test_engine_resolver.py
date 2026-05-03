import pytest
from promptspec_engine import resolve_prompt_spec
from promptspec_model import PromptSlot, PromptSpec, PromptStrategy


def strategy() -> PromptStrategy:
    return PromptStrategy(
        render_strategy="plain",
        validation_strategy="strict",
        inspection_strategy="schema_bound",
    )


def spec(
    spec_id: str,
    slots: list[PromptSlot],
    *,
    parent_id: str | None = None,
    metadata: dict[str, object] | None = None,
) -> PromptSpec:
    return PromptSpec(
        id=spec_id,
        title=spec_id,
        parent_id=parent_id,
        slots=slots,
        strategy=strategy(),
        metadata=metadata or {},
    )


def test_resolver_inherits_parent_slots() -> None:
    parent = spec("parent", [PromptSlot(key="audience", type="role", value="Engineers")])
    child = spec(
        "child",
        [PromptSlot(key="task", type="task", value="Summarize")],
        parent_id="parent",
    )

    resolved = resolve_prompt_spec(child, {"parent": parent})

    assert [slot.key for slot in resolved.slots] == ["audience", "task"]


def test_resolver_child_overrides_parent_same_key() -> None:
    parent = spec("parent", [PromptSlot(key="audience", type="role", value="Engineers")])
    child = spec(
        "child",
        [PromptSlot(key="audience", type="role", value="Researchers")],
        parent_id="parent",
    )

    resolved = resolve_prompt_spec(child, {"parent": parent})

    assert [slot.value for slot in resolved.slots] == ["Researchers"]


def test_resolver_filters_inactive_condition() -> None:
    prompt = spec(
        "spec",
        [
            PromptSlot(
                key="strict",
                type="constraint",
                value="Be strict",
                condition="mode == 'strict'",
            ),
            PromptSlot(
                key="loose",
                type="constraint",
                value="Be loose",
                condition="mode == 'loose'",
            ),
        ],
        metadata={"mode": "strict"},
    )

    resolved = resolve_prompt_spec(prompt)

    assert [slot.key for slot in resolved.slots] == ["strict"]


def test_resolver_applies_priority_conflict_groups() -> None:
    prompt = spec(
        "spec",
        [
            PromptSlot(key="brief", type="constraint", value="Be brief", priority=10),
            PromptSlot(key="detailed", type="constraint", value="Be detailed", priority=20),
        ],
        metadata={"conflict_groups": [["brief", "detailed"]]},
    )

    resolved = resolve_prompt_spec(prompt)

    assert [slot.key for slot in resolved.slots] == ["detailed"]


def test_resolver_requires_available_parent() -> None:
    child = spec("child", [], parent_id="missing")

    with pytest.raises(KeyError):
        resolve_prompt_spec(child, {})
