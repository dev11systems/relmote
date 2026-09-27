from __future__ import annotations

from dataclasses import dataclass

from .agent_access import (
    direct_transport_status,
    disable_direct_transport,
    enable_direct_transport,
)
from .runtime import RelmoteRuntime


@dataclass
class AgentAccessService:
    runtime: RelmoteRuntime

    def status(self) -> dict:
        transport = direct_transport_status(self.runtime)
        sessions = [
            grant.public()
            for grant in self.runtime.agent_grants.values()
            if grant.session.state.value != "ended"
        ]
        return {
            "transport": transport,
            "sessions": sessions,
            "enabled": bool(transport.get("enabled")),
        }

    def enable_transport(self) -> dict:
        result = enable_direct_transport(self.runtime)
        self.runtime.emit("agent.transport-enabled", {
            "kind": result.get("kind"),
            "address": result.get("bound_address"),
        })
        return self.status()

    def disable(self) -> dict:
        for grant in self.runtime.agent_grants.values():
            if grant.session.state.value != "ended":
                grant.session.revoke()
        try:
            disable_direct_transport(self.runtime)
        finally:
            self.runtime.emit("agent.access-disabled")
        return self.status()

    def create_session(
        self,
        workspace: str,
        capabilities: list[str],
        *,
        controller: str = "web-controller",
    ) -> dict:
        grant = self.runtime.request_agent(
            workspace,
            capabilities,
            controller=controller,
        )
        return grant.public()

    def approve_session(self, session_id: str) -> dict:
        grant = self.runtime.approve_agent(session_id)
        return grant.public()

    def pair_session(self, session_id: str) -> dict:
        return {
            "session_id": session_id,
            "code": self.runtime.create_agent_pairing(session_id),
            "expires_seconds": 300,
        }
