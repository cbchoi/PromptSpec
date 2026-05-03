import pytest
from promptspec_model import RenderedPrompt, Span
from pydantic import ValidationError


def test_span_accepts_canonical_fields() -> None:
    span = Span(slot_key="audience", start=29, end=54, text="senior backend engineers")

    assert span.slot_key == "audience"
    assert span.start == 29
    assert span.end == 54
    assert span.text == "senior backend engineers"


def test_span_rejects_negative_offsets() -> None:
    with pytest.raises(ValidationError):
        Span(slot_key="audience", start=-1, end=10, text="x")


def test_span_rejects_end_before_start() -> None:
    with pytest.raises(ValidationError):
        Span(slot_key="audience", start=10, end=9, text="x")


def test_rendered_prompt_accepts_spans() -> None:
    rendered = RenderedPrompt(
        spec_id="spec_001",
        text="Write for senior backend engineers.",
        spans=[Span(slot_key="audience", start=10, end=34, text="senior backend engineers")],
    )

    assert rendered.spec_id == "spec_001"
    assert rendered.spans[0].slot_key == "audience"

