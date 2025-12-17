#!/bin/bash

mkdir -p decision-control-plane/src/decision_control_plane/{core,infrastructure,governance,simulation,app}

touch decision-control-plane/README.md
touch decision-control-plane/requirements.txt
touch decision-control-plane/.gitignore

for dir in core infrastructure governance simulation app; do
  touch decision-control-plane/src/decision_control_plane/$dir/__init__.py
done

touch decision-control-plane/src/decision_control_plane/core/{types.py,ports.py,domain.py}
touch decision-control-plane/src/decision_control_plane/infrastructure/{clock.py,entropy.py}
touch decision-control-plane/src/decision_control_plane/governance/engine.py
touch decision-control-plane/src/decision_control_plane/simulation/stability.py
touch decision-control-plane/src/decision_control_plane/app/main.py

echo "✅ Repo initialized"
