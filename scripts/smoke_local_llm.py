from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
for source_path in (
    "packages/model/src",
    "packages/agents/src",
):
    sys.path.insert(0, str(ROOT / source_path))


def main() -> int:
    from promptspec_agents import LocalLLMInspector, OllamaClient
    from promptspec_model import RenderedPrompt

    inspector = LocalLLMInspector(OllamaClient())
    report = inspector.inspect(
        RenderedPrompt(spec_id="manual_smoke", text="Summarize the design.", spans=[])
    )
    print(report.model_dump_json(indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
