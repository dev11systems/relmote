from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any


PROTOCOL_VERSION = 1


class SafetyCommand(str, Enum):
    HELLO = "hello"
    QUERY_STATE = "query_state"
    BEGIN_SESSION = "begin_session"
    ARM_LEASE = "arm_lease"
    TYPE_TEXT = "type_text"
    RELEASE_ALL_KEYS = "release_all_keys"
    DISARM = "disarm"
    END_SESSION = "end_session"


@dataclass(frozen=True)
class SafetyMessage:
    """Logical message for the internal compute-to-safety boundary.

    This is intentionally NOT the final wire/crypto format.
    """

    command: SafetyCommand
    message_id: str
    session_id: str
    sequence: int
    lease_id: str | None = None
    payload: dict[str, Any] = field(default_factory=dict)
    protocol_version: int = PROTOCOL_VERSION

    def validate(self) -> None:
        if self.protocol_version != PROTOCOL_VERSION:
            raise ValueError("unsupported safety protocol version")
        if not self.message_id:
            raise ValueError("message_id is required")
        if not self.session_id:
            raise ValueError("session_id is required")
        if self.sequence < 0:
            raise ValueError("sequence must be non-negative")

        if self.command is SafetyCommand.TYPE_TEXT:
            self._validate_type_text()

    def _validate_type_text(self) -> None:
        if not self.lease_id:
            raise ValueError("type_text requires lease_id")

        text = self.payload.get("text")
        if not isinstance(text, str):
            raise ValueError("type_text payload requires string text")

        # Keep the safety-plane action smaller than the Linux HID maximum.
        # Longer text can be chunked into separately authorized messages.
        if len(text) > 128:
            raise ValueError("safety type_text exceeds 128 characters")


class ReplayWindow:
    """Minimal monotonic replay guard for one safety session.

    Persistence across MCU resets is deliberately outside this software model.
    """

    def __init__(self) -> None:
        self._last_sequence = -1

    @property
    def last_sequence(self) -> int:
        return self._last_sequence

    def accept(self, sequence: int) -> bool:
        if sequence <= self._last_sequence:
            return False
        self._last_sequence = sequence
        return True
