import numpy as np
from typing import Dict
from core.domain import ControlConfig
from core.ports import StabilityPort, EntropyPort


class MonteCarloStabilityAnalyzer(StabilityPort):
    def __init__(self, cfg: ControlConfig, entropy: EntropyPort):
        self.cfg = cfg
        self.entropy = entropy

    def confidence(
        self,
        candidate: str,
        scores: Dict[str, float],
        incumbent: str,
    ) -> float:
        policy_ids = list(self.cfg.policies.keys())

        base_scores = np.array([scores[p] for p in policy_ids])
        volatility = np.array(
            [self.cfg.policies[p].volatility for p in policy_ids]
        )

        noise = self.entropy.normal(
            mean=0.0,
            std=volatility,
            shape=(self.cfg.monte_carlo_runs, len(policy_ids)),
        )

        simulated = np.clip(base_scores + noise, 0.0, 1.0)

        penalties = np.array([
            0.0 if p == incumbent else self.cfg.hysteresis
            for p in policy_ids
        ])

        final_scores = simulated - penalties
        winners = np.argmax(final_scores, axis=1)

        return float(
            (winners == policy_ids.index(candidate)).mean()
        )
