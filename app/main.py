# Copyright 2026 Matías Salgado
# Licensed under the Apache License, Version 2.0.

from core.domain import ControlConfig, Policy
from core.enums import OperationalMode
from governance.engine import DecisionControlPlane
from infrastructure.clock import SystemClock
from infrastructure.entropy import NumpyEntropy
from simulation.stability import MonteCarloStabilityAnalyzer


def main() -> None:
    cfg = ControlConfig(
        mode=OperationalMode.AUTOMATIC,
        decision_threshold=0.75,
        hysteresis=0.07,
        min_stability=0.90,
        error_threshold=0.25,
        monte_carlo_runs=800,
        cooldown_minutes=10,
        policies={
            "tokyo": Policy("tokyo", 0.005, 0.01, 1),
            "berlin": Policy("berlin", 0.002, 0.06, 1),
            "istanbul": Policy("istanbul", 0.001, 0.10, 3),
        },
    )

    entropy = NumpyEntropy()
    clock = SystemClock()
    stability = MonteCarloStabilityAnalyzer(cfg, entropy)

    dcp = DecisionControlPlane(cfg, stability, clock)

    print("\nDECISION CONTROL PLANE REPORT")
    print("=" * 88)
    print(f"MODE            : {cfg.mode.value}")
    print("CONTROL TYPE    : DETERMINISTIC GOVERNANCE")
    print(f"ACTIVE PLATFORM : {dcp.state['current_policy']}")
    print("=" * 88)

    scores = {
        "tokyo": 0.82,
        "berlin": 0.95,
        "istanbul": 0.74,
    }

    errors = {
        "tokyo": 0.01,
        "berlin": 0.02,
        "istanbul": 0.05,
    }

    decision = dcp.evaluate(scores, errors)

    print(f"\nTRACE ID        : {decision['trace_id']}")
    print(f"DECISION        : {decision['decision']}")
    print(f"EVALUATED UNIT  : {decision['evaluated']}")
    print(f"EXECUTING UNIT  : {decision['executing']}")
    print(f"RATIONALE       : {decision['rationale']}")
    print(f"CONFIDENCE      : {decision['confidence']}%")

    print("\n" + "-" * 88)
    print(f"Estimated Net Savings : ${dcp.state['total_savings']:.2f} USD / month")
    print(f"FINAL OPERATING STATE : {dcp.state['current_policy']}")
    print("=" * 88)


if __name__ == "__main__":
    main()