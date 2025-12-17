from dataclasses import dataclass, field, asdict
from typing import Dict, Optional, Any
from datetime import datetime

from .types import PolicyID, TraceID, DecisionType

@dataclass(frozen=True)
class PolicyConfig:
    id: PolicyID
    base_score: float
    volatility: float
    priority: int

@dataclass(frozen=True)
class AppConfig:
    threshold: float = 0.75
    hysteresis: float = 0.10
    monte_carlo_runs: int = 5000
    policies: Dict[PolicyID, PolicyConfig] = field(default_factory=dict)

@dataclass(frozen=True)
class EvaluationContext:
    trace_id: TraceID
    current_provider: Optional[PolicyID]
    scores: Dict[PolicyID, float]

@dataclass(frozen=True)
class Decision:
    trace_id: TraceID
    selected_policy: PolicyID
    decision_type: DecisionType
    raw_score: float
    final_score: float
    reason: str
    metadata: Dict[str, Any]
    timestamp: str

    def log_json(self):
        import json
        print(f"AUDIT_LOG: {json.dumps(asdict(self))}")

