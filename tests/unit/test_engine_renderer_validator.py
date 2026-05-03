from promptspec_engine import render_prompt, validate_prompt
from promptspec_model import (
    MeaningReport,
    PromptSlot,
    PromptSpec,
    PromptStrategy,
    RenderedPrompt,
    Span,
)


def strategy() -> PromptStrategy:
    return PromptStrategy(
        render_strategy="plain",
        validation_strategy="strict",
        inspection_strategy="schema_bound",
    )


def spec(slots: list[PromptSlot], metadata: dict[str, object] | None = None) -> PromptSpec:
    return PromptSpec(
        id="spec_001",
        title="Spec",
        slots=slots,
        strategy=strategy(),
        metadata=metadata or {},
    )


def test_renderer_generates_text_and_spans() -> None:
    prompt = spec(
        [
            PromptSlot(key="audience", type="role", value="Write for engineers."),
            PromptSlot(key="task", type="task", value="Summarize the design."),
        ]
    )

    rendered = render_prompt(prompt)

    assert rendered.text == "Write for engineers.\nSummarize the design."
    assert rendered.spans[0].model_dump() == {
        "slot_key": "audience",
        "start": 0,
        "end": 20,
        "text": "Write for engineers.",
    }
    assert rendered.spans[1].start == 21


def test_validator_passes_renderer_output() -> None:
    prompt = spec([PromptSlot(key="task", type="task", value="Summarize the design.")])
    rendered = render_prompt(prompt)
    meaning = MeaningReport(spec_id="spec_001", meaning={"task": "summarize"})

    report = validate_prompt(prompt, rendered, meaning)

    assert report.status == "pass"
    assert report.metrics.slot_coverage == 1.0
    assert report.issues == []


def test_validator_flags_missing_required_slot() -> None:
    prompt = spec([PromptSlot(key="task", type="task", value="Summarize the design.")])
    rendered = RenderedPrompt(spec_id="spec_001", text="", spans=[])

    report = validate_prompt(prompt, rendered)

    assert report.status == "fail"
    assert report.issues[0].code == "MISSING_SLOT"


def test_validator_flags_declared_semantic_conflict() -> None:
    prompt = spec(
        [
            PromptSlot(key="brief", type="constraint", value="Be brief."),
            PromptSlot(key="detailed", type="constraint", value="Be detailed."),
        ],
        metadata={
            "conflicts": [
                {
                    "slot_keys": ["brief", "detailed"],
                    "message": "Cannot be both brief and detailed.",
                }
            ]
        },
    )

    report = validate_prompt(prompt, render_prompt(prompt))

    assert report.status == "fail"
    assert report.metrics.conflict_count == 1
    assert any(issue.code == "SEMANTIC_CONFLICT" for issue in report.issues)


def test_validator_flags_over_generation() -> None:
    prompt = spec([PromptSlot(key="task", type="task", value="Summarize the design.")])
    rendered = RenderedPrompt(
        spec_id="spec_001",
        text="Summarize the design. Add a joke.",
        spans=[Span(slot_key="task", start=0, end=21, text="Summarize the design.")],
    )

    report = validate_prompt(prompt, rendered)

    assert report.status == "fail"
    assert report.metrics.critical_over_generation == 1


def test_validator_flags_ambiguity_as_warning() -> None:
    prompt = spec([PromptSlot(key="task", type="task", value="Maybe summarize the design.")])
    report = validate_prompt(prompt, render_prompt(prompt))

    assert report.status == "pass"
    assert any(issue.code == "AMBIGUOUS_OUTPUT" for issue in report.issues)


def test_validator_flags_span_source_mismatch() -> None:
    prompt = spec([PromptSlot(key="task", type="task", value="Summarize the design.")])
    rendered = RenderedPrompt(
        spec_id="spec_001",
        text="Summarize the design.",
        spans=[Span(slot_key="task", start=0, end=21, text="Summarize")],
    )

    report = validate_prompt(prompt, rendered)

    assert report.status == "fail"
    assert any(issue.code == "RENDER_OMISSION" for issue in report.issues)

