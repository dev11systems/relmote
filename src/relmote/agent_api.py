from __future__ import annotations

from .agent_executor import list_path, read_text, run_command
from .runtime import RelmoteRuntime


def bearer_token(headers) -> str:
    value = headers.get("Authorization", "")
    if not value.startswith("Bearer "):
        raise PermissionError("agent bearer token required")
    token = value[7:].strip()
    if not token:
        raise PermissionError("agent bearer token required")
    return token


def handle_get(runtime: RelmoteRuntime, headers, path: str) -> dict:
    grant = runtime.agent_by_token(bearer_token(headers))
    if path == "/api/v1/agent/session":
        return grant.public()
    raise KeyError("unknown agent GET endpoint")


def handle_post(
    runtime: RelmoteRuntime,
    headers,
    path: str,
    payload: dict,
) -> dict:
    grant = runtime.agent_by_token(bearer_token(headers))
    session = grant.session

    if path == "/api/v1/agent/list":
        return {
            "entries": list_path(session, payload.get("path", ".")),
        }
    if path == "/api/v1/agent/read":
        return {
            "path": payload["path"],
            "text": read_text(session, payload["path"]),
        }
    if path == "/api/v1/agent/exec":
        argv = payload.get("argv")
        if not isinstance(argv, list) or not all(isinstance(x, str) for x in argv):
            raise ValueError("argv must be a list of strings")
        return run_command(
            session,
            argv,
            relative_cwd=payload.get("cwd", "."),
            timeout=int(payload.get("timeout", 30)),
        )
    raise KeyError("unknown agent POST endpoint")
