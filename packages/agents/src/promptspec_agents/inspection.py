"""Schema-bound local LLM meaning inspection."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Protocol

import httpx
from promptspec_model import MeaningReport, RenderedPrompt


class LLMClient(Protocol):
    def generate(self, prompt: str) -> str: ...


class OllamaClient:
    """Minimal Ollama-compatible generate client."""

    def __init__(
        self,
        endpoint: str = "http://localhost:11434",
        model: str = "llama3.1",
        timeout: float = 30.0,
        client: httpx.Client | None = None,
    ) -> None:
        self.endpoint = endpoint.rstrip("/")
        self.model = model
        self.timeout = timeout
        self.client = client or httpx.Client(timeout=timeout)

    def generate(self, prompt: str) -> str:
        response = self.client.post(
            f"{self.endpoint}/api/generate",
            json={"model": self.model, "prompt": prompt, "stream": False},
            timeout=self.timeout,
        )
        response.raise_for_status()
        payload = response.json()
        raw = payload.get("response")
        if not isinstance(raw, str):
            raise ValueError("LLM response missing string 'response' field")
        return raw


class LocalLLMInspector:
    """Inspects rendered prompts through a schema-bound local LLM prompt."""

    def __init__(
        self,
        client: LLMClient,
        trace_dir: Path = Path("reports/agents"),
    ) -> None:
        self.client = client
        self.trace_dir = trace_dir

    def inspect(self, rendered_prompt: RenderedPrompt) -> MeaningReport:
        prompt = build_inspection_prompt(rendered_prompt)
        raw_model = self.client.generate(prompt)
        report = meaning_report_from_raw(rendered_prompt.spec_id, raw_model)
        self._write_trace(rendered_prompt, prompt, raw_model, report)
        return report

    def _write_trace(
        self,
        rendered_prompt: RenderedPrompt,
        prompt: str,
        raw_model: str,
        report: MeaningReport,
    ) -> Path:
        self.trace_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%S%fZ")
        path = self.trace_dir / f"inspection_{rendered_prompt.spec_id}_{timestamp}.json"
        path.write_text(
            json.dumps(
                {
                    "spec_id": rendered_prompt.spec_id,
                    "prompt": prompt,
                    "rendered_prompt": rendered_prompt.model_dump(),
                    "raw_model": raw_model,
                    "meaning_report": report.model_dump(),
                },
                indent=2,
            )
        )
        return path


def build_inspection_prompt(rendered_prompt: RenderedPrompt) -> str:
    return (
        "You are a schema-bound meaning inspector.\n"
        "Return JSON only with this shape:\n"
        '{"meaning": {}, "uncertainties": []}\n'
        "Do not include markdown or prose.\n\n"
        f"Rendered prompt:\n{rendered_prompt.text}"
    )


def meaning_report_from_raw(spec_id: str, raw_model: str) -> MeaningReport:
    try:
        parsed = _extract_json_object(raw_model)
        meaning = parsed.get("meaning")
        uncertainties = parsed.get("uncertainties", [])
        if not isinstance(meaning, dict):
            raise ValueError("meaning must be an object")
        if not isinstance(uncertainties, list) or not all(
            isinstance(item, str) for item in uncertainties
        ):
            raise ValueError("uncertainties must be a list of strings")
        return MeaningReport(
            spec_id=spec_id,
            meaning=meaning,
            uncertainties=uncertainties,
            raw_model=raw_model,
        )
    except (json.JSONDecodeError, ValueError) as exc:
        return MeaningReport(
            spec_id=spec_id,
            meaning={},
            uncertainties=[f"SCHEMA_VIOLATION: {exc}"],
            raw_model=raw_model,
        )


def _extract_json_object(raw_model: str) -> dict[str, Any]:
    start = raw_model.find("{")
    end = raw_model.rfind("}")
    if start == -1 or end == -1 or end < start:
        raise ValueError("no JSON object found")
    parsed = json.loads(raw_model[start : end + 1])
    if not isinstance(parsed, dict):
        raise ValueError("top-level JSON must be an object")
    return parsed

