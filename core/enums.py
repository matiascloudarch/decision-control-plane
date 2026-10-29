# Copyright 2026 Matías Salgado
# Licensed under the Apache License, Version 2.0.

from enum import Enum


class OperationalMode(str, Enum):
    SHADOW = "SHADOW"
    AUTOMATIC = "AUTOMATIC"


class DecisionType(str, Enum):
    SWITCH = "SWITCH"
    MAINTAIN = "MAINTAIN"
    DENY_CHANGE = "DENY_CHANGE"
    QUARANTINE = "QUARANTINE"