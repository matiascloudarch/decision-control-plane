# decision-control-plane

**A decision control plane for governing AI infrastructure under uncertainty.**

`decision-control-plane` is a lightweight, deterministic governance kernel designed to
make **infrastructure-level decisions for AI systems** under noisy, uncertain, and dynamic conditions.

It models how an AI Platform / MLOps system can:
- arbitrate between multiple infrastructure or policy options
- apply hysteresis and stability guarantees
- prevent flapping and unsafe switches
- project future stability using Monte Carlo simulation

This project is intentionally **dependency-free**, **auditable**, and **deterministic by design**.

---

## Why this project exists

Modern AI platforms rely on:
- multiple cloud providers
- multiple models / endpoints
- dynamic cost, latency, and reliability signals

Yet most systems lack a **formal decision layer**.

`decision-control-plane` acts as that layer.

It is inspired by:
- Kubernetes control planes
- FinOps policy engines
- AI platform governance
- safety-first system design

---

## Architecture

**Hexagonal Architecture (Ports & Adapters)**

decision-control-plane/
│
├── core/ # Pure domain (no infrastructure)
│ ├── types.py
│ ├── ports.py
│ └── domain.py
│
├── governance/ # Decision engine
│ └── engine.py
│
├── simulation/ # Monte Carlo stability projection
│ └── stability.py
│
├── infrastructure/ # Adapters (clock, entropy)
│ ├── clock.py
│ └── entropy.py
│
└── app/
└── main.py # Demo / entrypoint

yaml

---

## Key concepts

- **Decision Control Plane**  
  A deterministic layer that decides *when* and *why* to switch infrastructure or policies.

- **Hysteresis & Stability**  
  Prevents noisy metrics from causing oscillations.

- **Monte Carlo Projection**  
  Quantifies long-term stability and risk.

- **Auditability**  
  Every decision emits structured JSON logs.

---

## Example output

```json
AUDIT_LOG: {
  "trace_id": "tx-999",
  "selected_policy": "tokyo",
  "decision_type": "MAINTAIN",
  "raw_score": 0.84,
  "final_score": 0.82,
  "reason": "Optimización de política",
  "metadata": {"p_vol": 0.02, "p_hys": 0.0},
  "timestamp": "2025-12-17T21:35:11Z"
}
Intended audience
AI Platform Engineers

MLOps Engineers

AI Architects

Infrastructure / FinOps Engineers

Author
Built by Matías Salgado
AI Platform / MLOps / Infrastructure Architecture

This project is part of a continuous portfolio focused on:
AI governance, cost control, and resilient system design.
