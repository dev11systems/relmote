from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4


class TerminalAuthority(str, Enum):
    USER = "user"
    ADMIN = "admin"


class TerminalState(str, Enum):
    REQUESTED = "requested"
    ACTIVE = "active"
    ENDED = "ended"
    DENIED = "denied"


@dataclass
class TerminalSession:
    target: str
    authority: TerminalAuthority = TerminalAuthority.USER
    controller: str = "local-controller"
    session_id: str = field(default_factory=lambda: str(uuid4()))
    state: TerminalState = TerminalState.REQUESTED

    @property
    def requires_approval(self) -> bool:
        # Interactive terminal access is always explicit in the preview.
        return True

    def approve(self) -> None:
        if self.state is not TerminalState.REQUESTED:
            raise ValueError("terminal session is not awaiting approval")
        self.state = TerminalState.ACTIVE

    def deny(self) -> None:
        if self.state is not TerminalState.REQUESTED:
            raise ValueError("terminal session is not awaiting approval")
        self.state = TerminalState.DENIED

    def end(self) -> None:
        if self.state is not TerminalState.ACTIVE:
            raise ValueError("only an active terminal can be ended")
        self.state = TerminalState.ENDED

    def revoke(self) -> None:
        if self.state in {TerminalState.REQUESTED, TerminalState.ACTIVE}:
            self.state = TerminalState.ENDED
