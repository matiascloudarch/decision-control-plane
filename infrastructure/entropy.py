import numpy as np
from core.ports import EntropyPort


class NumpyEntropy(EntropyPort):
    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)

    def normal(self, mean: float, std: float, shape):
        return self.rng.normal(mean, std, shape)
