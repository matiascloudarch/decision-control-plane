from decision_control_plane.infrastructure.clock import SystemClock
from decision_control_plane.infrastructure.entropy import DeterministicRNG
from decision_control_plane.core.domain import AppConfig, PolicyConfig, EvaluationContext
from decision_control_plane.core.types import PolicyID, TraceID
from decision_control_plane.governance.engine import GovernanceEngine
from decision_control_plane.simulation.stability import StabilityAnalyzer

def main():
    clock = SystemClock()
    rng = DeterministicRNG(seed_val=12345)

    cfg = AppConfig(policies={
        PolicyID("tokyo"):    PolicyConfig(PolicyID("tokyo"), 0.85, 0.02, 2),
        PolicyID("berlin"):   PolicyConfig(PolicyID("berlin"), 0.88, 0.04, 3),
        PolicyID("istanbul"): PolicyConfig(PolicyID("istanbul"), 0.78, 0.08, 1),
    })

    engine = GovernanceEngine(cfg, clock)
    analyzer = StabilityAnalyzer(engine, rng)

    ctx = EvaluationContext(
        TraceID("tx-999"),
        PolicyID("tokyo"),
        {
            PolicyID("tokyo"): 0.84,
            PolicyID("berlin"): 0.92,
            PolicyID("istanbul"): 0.75
        }
    )

    decision = engine.evaluate(ctx)
    decision.log_json()

    print("\n[STABILITY PROJECTION]")
    stats = analyzer.project(decision.selected_policy)
    for k, v in sorted(stats.items(), key=lambda x: -x[1]):
        bar = "█" * int(v / 2)
        print(f"{str(k):<12} | {bar} {v:.1f}%")

if __name__ == "__main__":
    main()

