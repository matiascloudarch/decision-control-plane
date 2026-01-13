import json
import random
from pathlib import Path
from datetime import timedelta
from typing import Dict

from core.domain import ControlConfig
from core.types import DecisionType, OperationalMode
from core.ports import StabilityPort, ClockPort


STATE_FILE = Path("control_plane_state.json")


class DecisionControlPlane:
    def __init__(
        self,
        cfg: ControlConfig,
        stability: StabilityPort,
        clock: ClockPort,
    ):
        self.cfg = cfg
        self.stability = stability
        self.clock = clock
        self.state = self._load_state()

    def _load_state(self):
        default = {
            "current_policy": "tokyo",
            "last_switch": None,
            "total_savings": 0.0,
        }

        if not STATE_FILE.exists():
            return default

        try:
            return json.loads(STATE_FILE.read_text())
        except Exception:
            return default

    def _save_state(self):
        tmp = STATE_FILE.with_suffix(".tmp")
        tmp.write_text(json.dumps(self.state, indent=2))
        tmp.replace(STATE_FILE)

    def _cooldown_active(self):
        if not self.state["last_switch"]:
            return False
        last = self.clock.now().fromisoformat(self.state["last_switch"])
        return self.clock.now() - last < timedelta(
            minutes=self.cfg.cooldown_minutes
        )

    def evaluate(
        self,
        scores: Dict[str, float],
        error_rates: Dict[str, float],
    ) -> dict:

        incumbent = self.state["current_policy"]

        # Hard safety gate
        for pid, err in error_rates.items():
            if err > self.cfg.error_threshold:
                return self._decision(
                    DecisionType.QUARANTINE,
                    incumbent,
                    incumbent,
                    "Error rate exceeds safety envelope.",
                    1.0,
                )

        viable = []
        for pid, score in scores.items():
            if score < self.cfg.decision_threshold:
                continue
            penalty = 0.0 if pid == incumbent else self.cfg.hysteresis
            viable.append((pid, score - penalty))

        viable.sort(key=lambda x: x[1], reverse=True)

        if not viable or viable[0][0] == incumbent:
            return self._decision(
                DecisionType.MAINTAIN,
                incumbent,
                incumbent,
                "Incumbent configuration remains optimal.",
                1.0,
            )

        candidate = viable[0][0]

        if self._cooldown_active():
            return self._decision(
                DecisionType.DENY_CHANGE,
                candidate,
                incumbent,
                "Cooldown active. Change deferred.",
                1.0,
            )

        confidence = self.stability.confidence(
            candidate, scores, incumbent
        )

        if confidence < self.cfg.min_stability:
            return self._decision(
                DecisionType.DENY_CHANGE,
                candidate,
                incumbent,
                "Projected instability exceeds acceptable bounds.",
                confidence,
            )

        if self.cfg.mode == OperationalMode.SHADOW:
            return self._decision(
                DecisionType.MAINTAIN,
                candidate,
                incumbent,
                "Shadow mode: execution suppressed.",
                confidence,
            )

        savings = (
            self.cfg.policies[incumbent].base_cost
            - self.cfg.policies[candidate].base_cost
        )

        self.state["total_savings"] += max(0.0, savings)
        self.state["current_policy"] = candidate
        self.state["last_switch"] = self.clock.now().isoformat()
        self._save_state()

        return self._decision(
            DecisionType.SWITCH,
            candidate,
            candidate,
            "Change authorized within stability envelope.",
            confidence,
        )

    def _decision(
        self,
        dtype: DecisionType,
        evaluated: str,
        executing: str,
        rationale: str,
        confidence: float,
    ):
        return {
            "trace_id": f"tx-{random.randint(100000,999999)}",
            "decision": dtype.value,
            "evaluated": evaluated,
            "executing": executing,
            "rationale": rationale,
            "confidence": round(confidence * 100, 2),
        }
