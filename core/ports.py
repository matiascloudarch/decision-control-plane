from typing import Dict


class StabilityPort:
    def confidence(
        self,
        candidate: str,
        scores: Dict[str, float],
        incumbent: str,
    ) -> float:
        raise NotImplementedError


class ClockPort:
    def now(self):
        raise NotImplementedError


class EntropyPort:
    def normal(self, mean: float, std: float, shape):
        raise NotImplementedError
