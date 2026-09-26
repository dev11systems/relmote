from __future__ import annotations

import time
from dataclasses import dataclass
from enum import Enum


class AvailabilityMode(str, Enum):
    DISABLED = "disabled"
    TIMED = "timed"
    UNTIL_DISABLED = "until-disabled"


@dataclass
class AccessPolicy:
    mode: AvailabilityMode = AvailabilityMode.DISABLED
    expires_at_monotonic: float | None = None

    def disable(self) -> None:
        self.mode = AvailabilityMode.DISABLED
        self.expires_at_monotonic = None

    def enable_until_disabled(self) -> None:
        self.mode = AvailabilityMode.UNTIL_DISABLED
        self.expires_at_monotonic = None

    def enable_for(
        self,
        seconds: float,
        *,
        clock=time.monotonic,
    ) -> None:
        if seconds <= 0:
            raise ValueError("seconds must be positive")
        self.mode = AvailabilityMode.TIMED
        self.expires_at_monotonic = clock() + seconds

    def available(self, *, clock=time.monotonic) -> bool:
        if self.mode is AvailabilityMode.DISABLED:
            return False
        if self.mode is AvailabilityMode.UNTIL_DISABLED:
            return True
        assert self.expires_at_monotonic is not None
        if clock() >= self.expires_at_monotonic:
            self.disable()
            return False
        return True
