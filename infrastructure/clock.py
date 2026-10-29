# Copyright 2026 Matías Salgado
# Licensed under the Apache License, Version 2.0.

from datetime import datetime, timezone

from core.ports import ClockPort


class SystemClock(ClockPort):
    def now(self) -> datetime:
        return datetime.now(timezone.utc)