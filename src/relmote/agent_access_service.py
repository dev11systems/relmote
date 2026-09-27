from __future__ import annotations

from dataclasses import dataclass

from .agent_access import (
    disable_private_transport,
    enable_private_transport,
    serve_status,
)
from .runtime import RelmoteRuntime


@dataclass
class AgentAccessService:
    runtime: RelmoteRuntime

    def status(self) -> dict:
        transport = serve_status()
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
        result = enable_private_transport()
        self.runtime.emit("agent.transport-enabled", {
            "kind": result.get("kind"),
        })
        return self.status()

    def disable(self) -> dict:
        # Disable authority first, then remove remote reachability.
        for grant in self.runtime.agent_grants.values():
            if grant.session.state.value != "ended":
                grant.session.revoke()
        try:
            disable_private_transport()
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
