# Copyright 2026 Matías Salgado
# Licensed under the Apache License, Version 2.0.

import pytest

from core.domain import ControlConfig, Policy
from core.enums import OperationalMode
from governance.evaluator import PolicyEvaluator


@pytest.fixture
def eval_config() -> ControlConfig:
    return ControlConfig(
        mode=OperationalMode.AUTOMATIC,
        decision_threshold=0.75,
        hysteresis=0.07,
        min_stability=0.90,
        error_threshold=0.25,
        monte_carlo_runs=100,
        cooldown_minutes=10,
        policies={
            "tokyo": Policy("tokyo", 0.005, 0.01, 1),
            "berlin": Policy("berlin", 0.002, 0.06, 1),
        },
    )


def test_evaluator_filters_below_threshold(eval_config: ControlConfig) -> None:
    evaluator = PolicyEvaluator(eval_config)
    scores = {"tokyo": 0.70, "berlin": 0.60}
    viable = evaluator.evaluate_viable(scores, incumbent="tokyo")
    assert len(viable) == 0


def test_evaluator_applies_hysteresis_penalty(
    eval_config: ControlConfig,
) -> None:
    evaluator = PolicyEvaluator(eval_config)
    scores = {"tokyo": 0.80, "berlin": 0.85}
    viable = evaluator.evaluate_viable(scores, incumbent="tokyo")
    assert viable[0][0] == "tokyo"