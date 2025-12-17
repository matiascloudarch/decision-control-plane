from enum import Enum
from typing import NewType

PolicyID = NewType("PolicyID", str)
TraceID = NewType("TraceID", str)

class DecisionType(str, Enum):
    SWITCH = "SWITCH"
    MAINTAIN = "MAINTAIN"
    BLOCKED = "BLOCKED"
    EMERGENCY_STOP = "EMERGENCY_STOP"
