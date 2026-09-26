from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from uuid import uuid4


class ScreenAuthority(str, Enum):
    OBSERVE = "observe"
    CONTROL = "control"


class ScreenState(str, Enum):
    REQUESTED = "requested"
    APPROVED = "approved"
    OS_CONSENT = "os-consent"
    ACTIVE = "active"
    ENDED = "ended"
    FAILED = "failed"


@dataclass
class ScreenSession:
    controller: str = "remote-controller"
    authority: ScreenAuthority = ScreenAuthority.OBSERVE
    session_id: str = ""
    state: ScreenState = ScreenState.REQUESTED
    error: str | None = None

    def __post_init__(self):
        if not self.session_id:
            self.session_id = str(uuid4())

    def approve(self) -> None:
        if self.state is not ScreenState.REQUESTED:
            raise ValueError("screen session is not awaiting approval")
        self.state = ScreenState.APPROVED

    def awaiting_os_consent(self) -> None:
        if self.state is not ScreenState.APPROVED:
            raise ValueError("screen session is not approved")
        self.state = ScreenState.OS_CONSENT

    def activate(self) -> None:
        if self.state is not ScreenState.OS_CONSENT:
            raise ValueError("screen session is not awaiting OS consent")
        self.state = ScreenState.ACTIVE

    def fail(self, message: str) -> None:
        self.error = message
        self.state = ScreenState.FAILED

    def revoke(self) -> None:
        if self.state not in {ScreenState.ENDED, ScreenState.FAILED}:
            self.state = ScreenState.ENDED
