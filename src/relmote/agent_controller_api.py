from __future__ import annotations

from .agent_controller import approve, create_request, revoke
from .runtime import RelmoteRuntime


PREFIX = "/api/v1/controller/agent"


def handle(runtime: RelmoteRuntime, path: str, payload: dict) -> tuple[int, dict]:
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
        return 200, {
            "session_id": session_id,
            "code": runtime.create_agent_pairing(session_id),
            "expires_seconds": 300,
        }
    raise KeyError("unknown agent controller action")
