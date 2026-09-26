from __future__ import annotations

import time
from dataclasses import dataclass
from typing import Protocol

from .safety import SafetyGate


class GPIOBackend(Protocol):
    def setup_input_pullup(self, pin: int) -> None: ...
    def setup_output(self, pin: int) -> None: ...
    def read(self, pin: int) -> bool: ...
    def write(self, pin: int, value: bool) -> None: ...


@dataclass(frozen=True)
class ControlPins:
    authorize: int = 17
    stop: int = 27
    armed_led: int = 22
    activity_led: int = 23


class PhysicalControls:
    """Bind prototype buttons/LEDs to SafetyGate.

    Buttons are active-low with pull-ups. AUTHORIZE clears a latched STOP on
    the first press but does not arm until a subsequent press.
    """

    def __init__(
        self,
        gpio: GPIOBackend,
        gate: SafetyGate,
        *,
        pins: ControlPins = ControlPins(),
        lease_seconds: float = 15.0,
        debounce_seconds: float = 0.05,
        clock=time.monotonic,
    ) -> None:
        self.gpio = gpio
        self.gate = gate
        self.pins = pins
        self.lease_seconds = lease_seconds
        self.debounce_seconds = debounce_seconds
        self.clock = clock
        self._last_authorize = True
        self._last_stop = True
        self._last_authorize_at = float("-inf")
        self._last_stop_at = float("-inf")

    def setup(self) -> None:
        self.gpio.setup_input_pullup(self.pins.authorize)
        self.gpio.setup_input_pullup(self.pins.stop)
        self.gpio.setup_output(self.pins.armed_led)
        self.gpio.setup_output(self.pins.activity_led)
        self.gpio.write(self.pins.armed_led, False)
        self.gpio.write(self.pins.activity_led, False)

    def poll(self) -> None:
        now = self.clock()
        authorize = self.gpio.read(self.pins.authorize)
        stop = self.gpio.read(self.pins.stop)

        if (
            self._last_stop
            and not stop
            and now - self._last_stop_at >= self.debounce_seconds
        ):
            self.gate.latch_stop()
            self._last_stop_at = now

        if (
            self._last_authorize
            and not authorize
            and now - self._last_authorize_at >= self.debounce_seconds
        ):
            if self.gate.snapshot().stop_latched:
                self.gate.reset_stop()
            else:
                self.gate.arm_for(self.lease_seconds)
            self._last_authorize_at = now

        self._last_authorize = authorize
        self._last_stop = stop
        self.gpio.write(self.pins.armed_led, self.gate.snapshot().armed)

    def set_activity(self, active: bool) -> None:
        self.gpio.write(self.pins.activity_led, active)
