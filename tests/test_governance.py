# Copyright 2026 Matías Salgado
# Licensed under the Apache License, Version 2.0.

from datetime import datetime, timezone
from typing import Dict

import pytest

from core.domain import ControlConfig, Policy
from core.enums import DecisionType, OperationalMode
from core.ports import ClockPort, StabilityPort
from governance.engine import DecisionControlPlane


class MockClock(ClockPort):
    def __init__(self) -> None:
        self.current_time = datetime(2026, 1, 1, 12, 0, tzinfo=timezone.utc)

    def now(self) -> datetime:
        return self.current_time


class MockStability(StabilityPort):
    def __init__(self, confidence_score: float = 0.95):
        self.score = confidence_score

    def confidence(
        self, candidate: str, scores: Dict[str, float], incumbent: str
    ) -> float:
        return self.score


@pytest.fixture
def base_config() -> ControlConfig:
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


def test_quarantine_on_high_error(
    base_config: ControlConfig,
    tmp_path: pytest.TempPathFactory,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("governance.engine.STATE_FILE", tmp_path / "state.json")
    clock = MockClock()
    stability = MockStability()
    dcp = DecisionControlPlane(base_config, stability, clock)

    scores = {"tokyo": 0.80, "berlin": 0.90}
    errors = {"tokyo": 0.01, "berlin": 0.30}

    result = dcp.evaluate(scores, errors)
    assert result["decision"] == DecisionType.QUARANTINE.value


def test_maintain_when_hysteresis_prevents_switch(
    base_config: ControlConfig,
    tmp_path: pytest.TempPathFactory,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("governance.engine.STATE_FILE", tmp_path / "state.json")
    clock = MockClock()
    stability = MockStability()
    dcp = DecisionControlPlane(base_config, stability, clock)

    scores = {"tokyo": 0.80, "berlin": 0.85}
    errors = {"tokyo": 0.01, "berlin": 0.01}

    result = dcp.evaluate(scores, errors)
    assert result["decision"] == DecisionType.MAINTAIN.value


def test_successful_switch(
    base_config: ControlConfig,
    tmp_path: pytest.TempPathFactory,
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr("governance.engine.STATE_FILE", tmp_path / "state.json")
    clock = MockClock()
    stability = MockStability(confidence_score=0.95)
    dcp = DecisionControlPlane(base_config, stability, clock)

    scores = {"tokyo": 0.80, "berlin": 0.95}
    errors = {"tokyo": 0.01, "berlin": 0.01}

    result = dcp.evaluate(scores, errors)
    assert result["decision"] == DecisionType.SWITCH.value
    assert result["executing"] == "berlin"