from __future__ import annotations

import secrets
from dataclasses import dataclass, field

from .agent_session import AgentCapability, AgentSession
from .workspace import WorkspacePolicy
from .agent_scope import classify_scope


@dataclass
class AgentGrant:
    session: AgentSession
    token: str = field(default_factory=lambda: secrets.token_urlsafe(32))

    def public(self) -> dict:
        return {
            "session_id": self.session.session_id,
            "controller": self.session.controller,
            "workspace": str(self.session.workspace.root),
            "capabilities": sorted(cap.value for cap in self.session.capabilities),
            "state": self.session.state.value,
            "scope": classify_scope(str(self.session.workspace.root)),
        }


def create_grant(
    root: str,
    *,
    controller: str,
    capabilities: list[str],
    allowed_tools: frozenset[str] | None = None,
) -> AgentGrant:
    requested = frozenset(AgentCapability(value) for value in capabilities)
    writable = AgentCapability.WRITE in requested
    policy = WorkspacePolicy.create(
        root,
        allowed_tools=allowed_tools or frozenset({"git", "pytest"}),
        writable=writable,
    )
    return AgentGrant(
        session=AgentSession(
            workspace=policy,
            controller=controller,
            capabilities=requested,
        )
    )
