# Copyright 2026 Matías Salgado
# Licensed under the Apache License, Version 2.0.

from dataclasses import dataclass
from typing import Dict

from core.enums import OperationalMode


@dataclass(frozen=True)
class Policy:
    id: str
    base_cost: float
    volatility: float
    priority: int


@dataclass
class ControlConfig:
    mode: OperationalMode
    decision_threshold: float
    hysteresis: float
    min_stability: float
    error_threshold: float
    monte_carlo_runs: int
    cooldown_minutes: int
    policies: Dict[str, Policy]