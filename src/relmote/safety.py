from __future__ import annotations

import time
from collections.abc import Callable
from dataclasses import dataclass
from threading import RLock
from typing import Protocol


class OutputGate(Protocol):
    """Minimal physical/safety-plane contract for target output."""

    def permits_output(self) -> bool:
        ...

    def stop_requested(self) -> bool:
        ...


@dataclass(frozen=True)
class SafetySnapshot:
    armed: bool
    stop_latched: bool
    seconds_remaining: float


class SafetyGate:
    """Time-bounded, fail-closed output interlock.

    The gate starts disarmed. A STOP latches until explicitly reset, and reset
    leaves the gate disarmed so a second, explicit arm is always required.
    """

    def __init__(self, *, clock: Callable[[], float] = time.monotonic) -> None:
        self._clock = clock
        self._lock = RLock()
        self._armed_until = 0.0
        self._stop_latched = False

    def arm_for(self, seconds: float) -> bool:
        if seconds <= 0:
            raise ValueError("arm duration must be positive")

        with self._lock:
            if self._stop_latched:
                return False
            self._armed_until = self._clock() + seconds
            return True

    def disarm(self) -> None:
        with self._lock:
            self._armed_until = 0.0

    def latch_stop(self) -> None:
        with self._lock:
            self._stop_latched = True
            self._armed_until = 0.0

    def reset_stop(self) -> None:
        """Clear a latched STOP but remain disarmed.

        Hardware integrations should expose this only through an explicitly
        local/physical reset path.
        """
        with self._lock:
            self._stop_latched = False
            self._armed_until = 0.0

    def permits_output(self) -> bool:
        with self._lock:
            return (not self._stop_latched) and self._clock() < self._armed_until

    def stop_requested(self) -> bool:
        return not self.permits_output()

    def snapshot(self) -> SafetySnapshot:
        with self._lock:
            now = self._clock()
            remaining = max(0.0, self._armed_until - now)
            armed = (not self._stop_latched) and remaining > 0
            return SafetySnapshot(
                armed=armed,
                stop_latched=self._stop_latched,
                seconds_remaining=remaining,
            )
