from __future__ import annotations

import time
from collections.abc import Callable
from contextlib import contextmanager
from pathlib import Path
from typing import BinaryIO, Iterator

from relmote.model import Action

from .base import Transport, TransportCapabilities


LEFT_SHIFT = 0x02
EMPTY_REPORT = bytes(8)

# USB HID usage IDs for a US keyboard layout.
_BASE: dict[str, int] = {
    **{chr(ord("a") + i): 0x04 + i for i in range(26)},
    "1": 0x1E,
    "2": 0x1F,
    "3": 0x20,
    "4": 0x21,
    "5": 0x22,
    "6": 0x23,
    "7": 0x24,
    "8": 0x25,
    "9": 0x26,
    "0": 0x27,
    "\n": 0x28,
    "\t": 0x2B,
    " ": 0x2C,
    "-": 0x2D,
    "=": 0x2E,
    "[": 0x2F,
    "]": 0x30,
    "\\": 0x31,
    ";": 0x33,
    "'": 0x34,
    "`": 0x35,
    ",": 0x36,
    ".": 0x37,
    "/": 0x38,
}

_SHIFTED: dict[str, str] = {
    "!": "1",
    "@": "2",
    "#": "3",
    "$": "4",
    "%": "5",
    "^": "6",
    "&": "7",
    "*": "8",
    "(": "9",
    ")": "0",
    "_": "-",
    "+": "=",
    "{": "[",
    "}": "]",
    "|": "\\",
    ":": ";",
    '"': "'",
    "~": "`",
    "<": ",",
    ">": ".",
    "?": "/",
}


def encode_character(character: str) -> tuple[int, int]:
    """Return (modifier, usage_id) for one supported US-keyboard character."""

    if len(character) != 1:
        raise ValueError("encode_character expects exactly one character")

    if "A" <= character <= "Z":
        return LEFT_SHIFT, _BASE[character.lower()]

    if character in _SHIFTED:
        return LEFT_SHIFT, _BASE[_SHIFTED[character]]

    if character in _BASE:
        return 0, _BASE[character]

    raise ValueError(f"unsupported keyboard character: {character!r}")


def keyboard_report(character: str) -> bytes:
    modifier, usage = encode_character(character)
    return bytes((modifier, 0, usage, 0, 0, 0, 0, 0))


class LinuxHIDKeyboardTransport(Transport):
    """Narrow Linux USB-gadget keyboard transport.

    This transport intentionally supports only the structured `type_text`
    action and the `input.keyboard` capability. It does not expose arbitrary
    HID reports.

    A caller-supplied stop predicate is checked before every character. If it
    becomes true, the transport emits only a key-release report and stops.
    """

    def __init__(
        self,
        device_path: str | Path = "/dev/hidg0",
        *,
        key_delay: float = 0.015,
        max_text_length: int = 512,
        stop_requested: Callable[[], bool] | None = None,
        device: BinaryIO | None = None,
    ) -> None:
        if key_delay < 0:
            raise ValueError("key_delay must be non-negative")
        if max_text_length <= 0:
            raise ValueError("max_text_length must be positive")

        self.device_path = Path(device_path)
        self.key_delay = key_delay
        self.max_text_length = max_text_length
        self.stop_requested = stop_requested or (lambda: False)
        self._injected_device = device

    @property
    def capabilities(self) -> TransportCapabilities:
        return TransportCapabilities(
            name="linux-usb-hid-keyboard",
            bidirectional=False,
            interactive=True,
            works_before_os=True,
        )

    @contextmanager
    def _device(self) -> Iterator[BinaryIO]:
        if self._injected_device is not None:
            yield self._injected_device
            return

        with self.device_path.open("wb", buffering=0) as handle:
            yield handle

    @staticmethod
    def _validate(action: Action, max_text_length: int) -> str:
        if action.kind != "type_text":
            raise ValueError("Linux HID transport only accepts type_text actions")

        if action.capabilities != ("input.keyboard",):
            raise ValueError(
                "type_text must request exactly the input.keyboard capability"
            )

        text = action.payload.get("text")
        if not isinstance(text, str):
            raise ValueError("type_text payload must contain a string 'text' field")

        if len(text) > max_text_length:
            raise ValueError(
                f"text length {len(text)} exceeds limit {max_text_length}"
            )

        # Validate the complete action before opening the target device so an
        # unsupported character cannot cause a partial prefix to be typed.
        for character in text:
            encode_character(character)

        return text

    def execute(self, action: Action) -> object:
        text = self._validate(action, self.max_text_length)
        sent = 0
        interrupted = False
        error: str | None = None

        try:
            with self._device() as device:
                for character in text:
                    if self.stop_requested():
                        interrupted = True
                        device.write(EMPTY_REPORT)
                        break

                    device.write(keyboard_report(character))
                    device.write(EMPTY_REPORT)
                    sent += 1

                    if self.key_delay:
                        time.sleep(self.key_delay)

        except OSError as exc:
            # Once dispatch has begun we do not raise: the controller consumes
            # the action ID rather than risking an automatic replay of a
            # partially emitted action.
            error = f"{type(exc).__name__}: {exc}"

        return {
            "transport": self.capabilities.name,
            "completed": sent == len(text) and not interrupted and error is None,
            "characters_requested": len(text),
            "characters_sent": sent,
            "interrupted": interrupted,
            "error": error,
        }
