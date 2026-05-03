import pytest
from promptspec_model import RalphTask
from pydantic import ValidationError


def test_ralph_task_accepts_canonical_fields() -> None:
    task = RalphTask(
        id="M1.T2",
        title="Implement PromptSlot model",
        status="pending",
        source_doc="docs/Data_Model.md",
        acceptance_criteria=["PromptSlot has canonical fields"],
        test_commands=["python -m pytest tests/unit/test_prompt_slot.py"],
        dependencies=["M1.T1"],
    )

    assert task.id == "M1.T2"
    assert task.status == "pending"
    assert task.dependencies == ["M1.T1"]


def test_ralph_task_rejects_invalid_status() -> None:
    with pytest.raises(ValidationError):
        RalphTask(
            id="M1.T2",
            title="Implement PromptSlot model",
            status="done",
            source_doc="docs/Data_Model.md",
            acceptance_criteria=["x"],
            test_commands=["pytest"],
        )


def test_ralph_task_rejects_missing_acceptance_criteria() -> None:
    with pytest.raises(ValidationError):
        RalphTask(
            id="M1.T2",
            title="Implement PromptSlot model",
            status="pending",
            source_doc="docs/Data_Model.md",
            test_commands=["pytest"],
        )


def test_ralph_task_rejects_missing_test_commands() -> None:
    with pytest.raises(ValidationError):
        RalphTask(
            id="M1.T2",
            title="Implement PromptSlot model",
            status="pending",
            source_doc="docs/Data_Model.md",
            acceptance_criteria=["x"],
        )

