from promptspec_engine import evaluate_condition


def test_empty_condition_is_active() -> None:
    assert evaluate_condition(None, {}) is True
    assert evaluate_condition("", {}) is True


def test_condition_flag_truthiness() -> None:
    assert evaluate_condition("enabled", {"enabled": True}) is True
    assert evaluate_condition("enabled", {"enabled": False}) is False


def test_condition_negation() -> None:
    assert evaluate_condition("not disabled", {"disabled": False}) is True
    assert evaluate_condition("!disabled", {"disabled": True}) is False


def test_condition_comparison() -> None:
    assert evaluate_condition("mode == 'strict'", {"mode": "strict"}) is True
    assert evaluate_condition("priority != 10", {"priority": 5}) is True
    assert evaluate_condition("enabled == true", {"enabled": True}) is True

