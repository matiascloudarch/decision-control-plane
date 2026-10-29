# Copyright 2026 Matías Salgado
# Licensed under the Apache License, Version 2.0.

from typing import Dict, List, Tuple

from core.domain import ControlConfig


class PolicyEvaluator:
    """
    Evaluates policy scores against thresholds and applies hysteresis penalties.
    """

    def __init__(self, cfg: ControlConfig):
        self.cfg = cfg

    def evaluate_viable(
        self, scores: Dict[str, float], incumbent: str
    ) -> List[Tuple[str, float]]:
        """
        Filters candidates above decision threshold and applies hysteresis penalty
        to non-incumbents. Returns a sorted list of viable candidates.
        """
        viable = []
        for pid, score in scores.items():
            if score < self.cfg.decision_threshold:
                continue
            penalty = 0.0 if pid == incumbent else self.cfg.hysteresis
            viable.append((pid, score - penalty))

        viable.sort(key=lambda x: x[1], reverse=True)
        return viable