from __future__ import annotations

from typing import Any


class GpioZeroBackend:
    """Optional adapter for gpiozero.

    gpiozero is imported lazily so ordinary Relmote installs and CI do not
    acquire a Raspberry-Pi-specific dependency.
    """

    def __init__(self) -> None:
        try:
            from gpiozero import Button, LED
        except ImportError as exc:
            raise RuntimeError(
                "gpiozero is not installed; install the Pi hardware extra"
            ) from exc

        self._Button = Button
        self._LED = LED
        self._inputs: dict[int, Any] = {}
        self._outputs: dict[int, Any] = {}

    def setup_input_pullup(self, pin: int) -> None:
        if pin not in self._inputs:
            self._inputs[pin] = self._Button(pin, pull_up=True, bounce_time=None)

    def setup_output(self, pin: int) -> None:
        if pin not in self._outputs:
            self._outputs[pin] = self._LED(pin)
            self._outputs[pin].off()

    def read(self, pin: int) -> bool:
        # PhysicalControls expects raw pull-up semantics:
        # True = released/high, False = pressed/low.
        return not self._inputs[pin].is_pressed

    def write(self, pin: int, value: bool) -> None:
        if value:
            self._outputs[pin].on()
        else:
            self._outputs[pin].off()

    def close(self) -> None:
        for device in [*self._inputs.values(), *self._outputs.values()]:
            device.close()
