from datetime import datetime, timezone
from core.ports import ClockPort


class SystemClock(ClockPort):
    def now(self):
        return datetime.now(timezone.utc)
