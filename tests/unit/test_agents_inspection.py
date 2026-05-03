from pathlib import Path

import httpx
from promptspec_agents import (
    LocalLLMInspector,
    OllamaClient,
    build_inspection_prompt,
    meaning_report_from_raw,
)
from promptspec_model import RenderedPrompt


class FakeClient:
    def __init__(self, raw: str) -> None:
        self.raw = raw

    def generate(self, prompt: str) -> str:
        assert "Rendered prompt:" in prompt
        return self.raw


def test_build_inspection_prompt_requires_json_only() -> None:
    prompt = build_inspection_prompt(
        RenderedPrompt(spec_id="spec_001", text="Summarize.", spans=[])
    )

    assert "Return JSON only" in prompt
    assert "Summarize." in prompt


def test_meaning_report_from_valid_raw_json() -> None:
    report = meaning_report_from_raw(
        "spec_001",
        '{"meaning": {"task": "summarize"}, "uncertainties": ["tone"]}',
    )

    assert report.meaning == {"task": "summarize"}
    assert report.uncertainties == ["tone"]


def test_meaning_report_from_invalid_raw_json_marks_schema_violation() -> None:
    report = meaning_report_from_raw("spec_001", "not json")

    assert report.meaning == {}
    assert report.uncertainties[0].startswith("SCHEMA_VIOLATION")


def test_local_llm_inspector_writes_trace(tmp_path: Path) -> None:
    inspector = LocalLLMInspector(
        FakeClient('{"meaning": {"task": "summarize"}, "uncertainties": []}'),
        trace_dir=tmp_path,
    )

    report = inspector.inspect(RenderedPrompt(spec_id="spec_001", text="Summarize.", spans=[]))

    assert report.meaning == {"task": "summarize"}
    assert list(tmp_path.glob("inspection_spec_001_*.json"))


def test_ollama_client_reads_generate_response() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        assert request.url.path == "/api/generate"
        return httpx.Response(200, json={"response": '{"meaning": {}, "uncertainties": []}'})

    client = httpx.Client(transport=httpx.MockTransport(handler))
    ollama = OllamaClient(endpoint="http://local-llm", model="test", client=client)

    assert ollama.generate("prompt") == '{"meaning": {}, "uncertainties": []}'

