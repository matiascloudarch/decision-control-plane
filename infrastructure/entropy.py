import random
from decision_control_plane.core.ports import EntropySource

class DeterministicRNG(EntropySource):
    def __init__(self, seed_val: int = 42):
        self._rng = random.Random(seed_val)

    def seed(self, val: int) -> None:
        self._rng.seed(val)

    def gauss(self, mu: float, sigma: float) -> float:
        return self._rng.gauss(mu, sigma)

