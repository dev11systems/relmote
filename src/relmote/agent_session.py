from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from uuid import uuid4

from .workspace import WorkspacePolicy


class AgentCapability(str, Enum):
    LIST = "workspace.list"
    READ = "workspace.read"
    WRITE = "workspace.write"
    EXEC = "terminal.exec"
    OBSERVE = "system.observe"


class AgentState(str, Enum):
    REQUESTED = "requested"
    ACTIVE = "active"
    ENDED = "ended"


@dataclass
class AgentSession:
    workspace: WorkspacePolicy
    controller: str
    capabilities: frozenset[AgentCapability]
    session_id: str = field(default_factory=lambda: str(uuid4()))
    state: AgentState = AgentState.REQUESTED

    def approve(self) -> None:
        if self.state is not AgentState.REQUESTED:
            raise ValueError("agent session is not awaiting approval")
        self.state = AgentState.ACTIVE

    def require(self, capability: AgentCapability) -> None:
        if self.state is not AgentState.ACTIVE:
            raise PermissionError("agent session is not active")
        if capability not in self.capabilities:
            raise PermissionError(f"agent capability not granted: {capability.value}")

    def revoke(self) -> None:
        self.state = AgentState.ENDED
