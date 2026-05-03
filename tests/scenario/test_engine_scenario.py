from promptspec_engine import render_prompt, resolve_prompt_spec, validate_prompt
from promptspec_model import PromptSlot, PromptSpec, PromptStrategy


def test_engine_resolve_render_validate_scenario() -> None:
    strategy = PromptStrategy(
        render_strategy="plain",
        validation_strategy="strict",
        inspection_strategy="schema_bound",
    )
    parent = PromptSpec(
        id="parent",
        title="Parent",
        strategy=strategy,
        slots=[PromptSlot(key="audience", type="role", value="Write for engineers.")],
    )
    child = PromptSpec(
        id="child",
        title="Child",
        parent_id="parent",
        strategy=strategy,
        slots=[PromptSlot(key="task", type="task", value="Summarize the architecture.")],
    )

    resolved = resolve_prompt_spec(child, {"parent": parent})
    rendered = render_prompt(resolved)
    report = validate_prompt(resolved, rendered)

    assert rendered.text == "Write for engineers.\nSummarize the architecture."
    assert report.status == "pass"

