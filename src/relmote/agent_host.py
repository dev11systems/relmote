from __future__ import annotations

import os
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
        for name in ("git", "python3", "pytest", "node", "npm", "docker", "podman")
        if shutil.which(name)
    )
    capabilities = [
        "relmote.controller",
        "relmote.agent-client",
    ]
    if "git" in detected_tools:
        capabilities.append("development.git")
    if "python3" in detected_tools:
        capabilities.append("development.python")
    if any(name in detected_tools for name in ("docker", "podman")):
        capabilities.append("containers")

    return AgentHost(
        name=socket.gethostname(),
        platform=platform.system().lower(),
        architecture=platform.machine(),
        capabilities=tuple(capabilities),
        tools=detected_tools,
    )
