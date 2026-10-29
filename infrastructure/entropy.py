# Copyright 2026 Matías Salgado
# Licensed under the Apache License, Version 2.0.

from typing import Any

import numpy as np

from core.ports import EntropyPort


class NumpyEntropy(EntropyPort):
    def __init__(self, seed: int = 42):
        self.rng = np.random.default_rng(seed)

    def normal(self, mean: float, std: Any, shape: Any) -> Any:
        return self.rng.normal(mean, std, shape)