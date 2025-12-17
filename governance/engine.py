from typing import Tuple, Dict
from datetime import timezone

from decision_control_plane.core.domain import (
    AppConfig, PolicyConfig, EvaluationContext, Decision
)
from decision_control_plane.core.types import DecisionType, PolicyID
from decision_control_plane.core.ports import Clock

class GovernanceEngine:
    def __init__(self, config: AppConfig, clock: Clock):
        self.cfg = config
        self.clock = clock

    def _apply_rules(
        self,
        policy: PolicyConfig,
        raw: float,
        is_incumbent: bool
    ) -> Tuple[float, Dict[str, float]]:
        penalty_vol = policy.volatility
        penalty_hys = 0.0 if is_incumbent else self.cfg.hysteresis
        final = raw - penalty_vol - penalty_hys
        return final, {"p_vol": penalty_vol, "p_hys": penalty_hys}

    def evaluate(self, ctx: EvaluationContext) -> Decision:
        ts = self.clock.now().isoformat()

        if not ctx.scores:
            return Decision(
                ctx.trace_id,
                PolicyID(ctx.current_provider or "NONE"),
                DecisionType.EMERGENCY_STOP,
                0.0,
                0.0,
                "Telemetry blackout",
                {},
                ts
            )

        candidates = []

        for pid, policy in self.cfg.policies.items():
            raw = ctx.scores.get(pid, 0.0)
            if raw < self.cfg.threshold:
                continue

            is_incumbent = pid == ctx.current_provider
            final, factors = self._apply_rules(policy, raw, is_incumbent)

            candidates.append({
                "pid": pid,
                "raw": raw,
                "final": final,
                "priority": policy.priority,
                "is_incumbent": is_incumbent,
                "factors": factors
            })

        candidates.sort(
            key=lambda x: (x["final"], x["priority"], x["is_incumbent"]),
            reverse=True
        )

        if not candidates:
            return Decision(
                ctx.trace_id,
                PolicyID(ctx.current_provider or "NONE"),
                DecisionType.MAINTAIN if ctx.current_provider else DecisionType.BLOCKED,
                0.0,
                0.0,
                "No candidates above threshold",
                {},
                ts
            )

        winner = candidates[0]
        decision_type = (
            DecisionType.SWITCH
            if winner["pid"] != ctx.current_provider
            else DecisionType.MAINTAIN
        )

        return Decision(
            ctx.trace_id,
            winner["pid"],
            decision_type,
            winner["raw"],
            winner["final"],
            "Policy optimization",
            winner["factors"],
            ts
        )

