from promptspec_harness import compare_meaning


def test_compare_meaning_passes_matching_values() -> None:
    result = compare_meaning({"task": "summarize"}, {"task": "summarize"})

    assert result.status == "pass"


def test_compare_meaning_reports_missing_and_mismatched_keys() -> None:
    result = compare_meaning({"task": "summarize", "tone": "formal"}, {"task": "rewrite"})

    assert result.status == "fail"
    assert result.missing_keys == ["tone"]
    assert result.mismatched_keys == ["task"]

