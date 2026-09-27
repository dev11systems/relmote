from __future__ import annotations

import os
import subprocess
from pathlib import Path

from .agent_session import AgentCapability, AgentSession


def _root(session: AgentSession) -> Path:
    return Path(str(session.workspace.root)).resolve()


def _path(session: AgentSession, relative: str) -> Path:
    session.workspace.resolve_relative(relative)
    root = _root(session)
    candidate = (root / relative).resolve()
    try:
        candidate.relative_to(root)
    except ValueError as exc:
        raise ValueError("workspace path escapes configured root") from exc
    return candidate


def list_path(session: AgentSession, relative: str = ".") -> list[dict]:
    session.require(AgentCapability.LIST)
    path = _path(session, relative)
    if not path.is_dir():
        raise NotADirectoryError(relative)
    return [
        {
            "name": child.name,
            "type": "directory" if child.is_dir() else "file",
            "size": child.stat().st_size if child.is_file() else None,
        }
        for child in sorted(path.iterdir(), key=lambda p: p.name.lower())
    ]


def read_text(session: AgentSession, relative: str, *, max_bytes: int = 262144) -> str:
    session.require(AgentCapability.READ)
    path = _path(session, relative)
    data = path.read_bytes()
    if len(data) > max_bytes:
        raise ValueError(f"file exceeds read limit of {max_bytes} bytes")
    return data.decode("utf-8", errors="replace")


def run_command(
    session: AgentSession,
    argv: list[str],
    *,
    relative_cwd: str = ".",
    timeout: int = 30,
) -> dict:
    session.require(AgentCapability.EXEC)
    if not argv:
        raise ValueError("command argv cannot be empty")
    tool = os.path.basename(argv[0])
    session.workspace.require_tool(tool)
    cwd = _path(session, relative_cwd)
    if not cwd.is_dir():
        raise NotADirectoryError(relative_cwd)
    completed = subprocess.run(
        argv,
        cwd=cwd,
        capture_output=True,
        text=True,
        timeout=min(max(timeout, 1), 120),
        check=False,
        shell=False,
    )
    return {
        "argv": argv,
        "cwd": str(cwd),
        "returncode": completed.returncode,
        "stdout": completed.stdout[-262144:],
        "stderr": completed.stderr[-262144:],
    }
