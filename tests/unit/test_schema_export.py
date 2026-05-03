import json

from promptspec_model import export_json_schemas


def test_schema_export_includes_all_canonical_models() -> None:
    schemas = export_json_schemas()

    assert set(schemas) == {
        "PromptSlot",
        "PromptSpec",
        "RenderedPrompt",
        "MeaningReport",
        "ValidationReport",
        "TestReport",
        "RalphTask",
    }


def test_schema_export_is_json_serializable() -> None:
    json.dumps(export_json_schemas())

