"""Prompt rendering with span metadata."""

from __future__ import annotations

from promptspec_model import PromptSpec, RenderedPrompt, Span


def render_prompt(spec: PromptSpec) -> RenderedPrompt:
    """Render slot values into prompt text with exact source spans."""

    text_parts: list[str] = []
    spans: list[Span] = []
    cursor = 0

    for slot in spec.slots:
        if text_parts:
            text_parts.append("\n")
            cursor += 1
        start = cursor
        text_parts.append(slot.value)
        cursor += len(slot.value)
        spans.append(Span(slot_key=slot.key, start=start, end=cursor, text=slot.value))

    return RenderedPrompt(spec_id=spec.id, text="".join(text_parts), spans=spans)

