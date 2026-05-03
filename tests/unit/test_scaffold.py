from pathlib import Path


def test_initial_implementation_scaffold_exists() -> None:
    root = Path(__file__).resolve().parents[2]

    assert (root / "packages/model/src/promptspec_model").is_dir()
    assert (root / "tests/unit").is_dir()
    assert (root / "ralph/task_list.json").is_file()
    assert (root / "docs/implementation/Traceability_Matrix.md").is_file()

