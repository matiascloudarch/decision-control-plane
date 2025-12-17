from datetime import datetime, timezone
from decision_control_plane.core.ports import Clock

class SystemClock(Clock):
    def now(self) -> datetime:
        return datetime.now(timezone.utc)

