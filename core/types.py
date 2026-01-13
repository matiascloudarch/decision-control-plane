from enum import Enum


class OperationalMode(str, Enum):
    SHADOW = "SHADOW"
    AUTOMATIC = "AUTOMATIC"


class DecisionType(str, Enum):
    SWITCH = "SWITCH"
    MAINTAIN = "MAINTAIN"
    DENY_CHANGE = "DENY_CHANGE"
    QUARANTINE = "QUARANTINE"
