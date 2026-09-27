from __future__ import annotations

from .runtime import RelmoteRuntime


DEFAULT_CAPABILITIES = [
    "workspace.list",
    "workspace.read",
    "terminal.exec",
]


def create_request(runtime: RelmoteRuntime, payload: dict) -> dict:
    root = str(payload.get("workspace", "")).strip()
    if not root:
        raise ValueError("workspace is required")

    capabilities = payload.get("capabilities", DEFAULT_CAPABILITIES)
    if not isinstance(capabilities, list) or not all(
        isinstance(value, str) for value in capabilities
    ):
        raise ValueError("capabilities must be a list of strings")

    grant = runtime.request_agent(
        root,
        capabilities,
        controller=str(payload.get("controller") or "web-controller"),
    )
    return grant.public()


def approve(runtime: RelmoteRuntime, session_id: str) -> dict:
    grant = runtime.approve_agent(session_id)
    # The bearer token is intentionally returned only by this approval action.
    value = grant.public()
    value["token"] = grant.token
    return value


def revoke(runtime: RelmoteRuntime, session_id: str) -> dict:
    grant = runtime.revoke_agent(session_id)
    return grant.public()
