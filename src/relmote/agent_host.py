from __future__ import annotations

import platform
import shutil
import socket
from dataclasses import dataclass, asdict


@dataclass(frozen=True)
class AgentHost:
    name: str
    platform: str
    architecture: str
    capabilities: tuple[str, ...]
    tools: tuple[str, ...]

    def as_dict(self) -> dict:
        return asdict(self)


def detect_agent_host() -> AgentHost:
    detected_tools = tuple(
        name
        for name in (
            "git",
            "python3",
            "python",
            "pytest",
            "node",
            "npm",
            "codex",
            "docker",
            "podman",
        )
        if shutil.which(name)
    )
    capabilities = [
        "relmote.controller",
        "relmote.agent-client",
    ]
    if "git" in detected_tools:
        capabilities.append("development.git")
    if any(name in detected_tools for name in ("python3", "python")):
        capabilities.append("development.python")
    if "codex" in detected_tools:
        capabilities.append("development.codex")
    if any(name in detected_tools for name in ("docker", "podman")):
        capabilities.append("containers")

    return AgentHost(
        name=socket.gethostname(),
        platform=platform.system().lower(),
        architecture=platform.machine(),
        capabilities=tuple(capabilities),
        tools=detected_tools,
    )
