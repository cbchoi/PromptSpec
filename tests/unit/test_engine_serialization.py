from promptspec_engine import slots_from_json, slots_from_yaml, slots_to_json, slots_to_yaml
from promptspec_model import PromptSlot


def test_slots_round_trip_json() -> None:
    slots = [PromptSlot(key="audience", type="role", value="Senior engineers")]

    loaded = slots_from_json(slots_to_json(slots))

    assert loaded == slots


def test_slots_round_trip_yaml() -> None:
    slots = [PromptSlot(key="constraint", type="constraint", value="Use citations")]

    loaded = slots_from_yaml(slots_to_yaml(slots))

    assert loaded == slots

