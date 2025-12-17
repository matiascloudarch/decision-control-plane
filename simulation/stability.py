from collections import Counter
from decision_control_plane.core.types import TraceID, DecisionType
from decision_control_plane.core.domain import EvaluationContext
from decision_control_plane.core.types import PolicyID

class StabilityAnalyzer:
    def __init__(self, engine, rng):
        self.engine = engine
        self.rng = rng

    def project(self, start_node: PolicyID):
        outcomes = Counter()
        runs = self.engine.cfg.monte_carlo_runs
        policies = list(self.engine.cfg.policies.values())

        for i in range(runs):
            sim_scores = {
                p.id: max(0.0, min(1.0, self.rng.gauss(p.base_score, p.volatility)))
                for p in policies
            }

            ctx = EvaluationContext(
                TraceID(f"sim-{i}"),
                start_node,
                sim_scores
            )

            decision = self.engine.evaluate(ctx)
            key = (
                decision.selected_policy
                if decision.decision_type == DecisionType.SWITCH
                else "MAINTAIN"
            )
            outcomes[key] += 1

        return {k: (v / runs) * 100 for k, v in outcomes.items()}

