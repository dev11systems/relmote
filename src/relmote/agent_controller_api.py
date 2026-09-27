from __future__ import annotations

from .agent_controller import approve, create_request, revoke
from .runtime import RelmoteRuntime
from .agent_access_service import AgentAccessService
from .path_suggest import suggest_directories


PREFIX = "/api/v1/controller/agent"


def handle(runtime: RelmoteRuntime, path: str, payload: dict) -> tuple[int, dict]:
    access = AgentAccessService(runtime)

    if path == f"{PREFIX}/status":
        return 200, access.status()
    if path == f"{PREFIX}/suggest":
        query = str(payload.get("query", ""))
        return 200, {"suggestions": suggest_directories(query)}
    if path == f"{PREFIX}/enable":
        return 200, access.enable_transport()
    if path == f"{PREFIX}/disable":
        return 200, access.disable()
    if path == f"{PREFIX}/request":
        return 201, create_request(runtime, payload)

    parts = path.strip("/").split("/")
    # api/v1/controller/agent/<session-id>/<action>
    if len(parts) != 6 or parts[:4] != ["api", "v1", "controller", "agent"]:
        raise KeyError("unknown agent controller endpoint")

    session_id, action = parts[4], parts[5]
    if action == "approve":
        return 200, approve(runtime, session_id)
    if action == "revoke":
        return 200, revoke(runtime, session_id)
    if action == "pair":
        transport = access.status().get("transport", {})
        return 200, {
            "session_id": session_id,
            "code": runtime.create_agent_pairing(session_id),
            "expires_seconds": 300,
            "agent_url": transport.get("url"),
        }
    raise KeyError("unknown agent controller action")
