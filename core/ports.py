# Copyright 2026 Matías Salgado
# Licensed under the Apache License, Version 2.0.

from datetime import datetime
from typing import Any, Dict


class StabilityPort:
    def confidence(
        self,
        candidate: str,
        scores: Dict[str, float],
        incumbent: str,
    ) -> float:
        raise NotImplementedError


class ClockPort:
    def now(self) -> datetime:
        raise NotImplementedError


class EntropyPort:
    def normal(self, mean: float, std: Any, shape: Any) -> Any:
        raise NotImplementedError