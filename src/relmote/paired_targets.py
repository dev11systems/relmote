from __future__ import annotations

import json
from collections.abc import Callable

from .agent_client import RelmoteAgentClient
from .agent_profiles import load_profile, profile_directory


class PairedTargetService:
    """Operations over locally paired Relmote targets for an Agent Host.

    Profile credentials stay internal so human-facing and agent-facing adapters
    can share one target-operation boundary without returning bearer material.
    """

    def __init__(
        self,
        *,
        client_factory: Callable[[str, str], RelmoteAgentClient] = RelmoteAgentClient,
    ):
        self._client_factory = client_factory

    def _client(self, target: str) -> RelmoteAgentClient:
        profile = load_profile(target)
        return self._client_factory(profile["base_url"], profile["token"])

    def targets(self) -> list[dict]:
        directory = profile_directory()
        if not directory.exists():
            return []

        result: list[dict] = []
        for path in sorted(directory.glob("*.json")):
            try:
                profile = json.loads(path.read_text())
            except (OSError, json.JSONDecodeError):
                result.append(
                    {
                        "name": path.stem,
                        "workspace": None,
                        "state": "unreadable",
                        "capabilities": [],
                    }
                )
                continue

            session = profile.get("session")
            if not isinstance(session, dict):
                session = {}
            capabilities = session.get("capabilities")
            if not isinstance(capabilities, list):
                capabilities = []

            result.append(
                {
                    "name": profile.get("name") or path.stem,
                    "workspace": session.get("workspace"),
                    "state": session.get("state"),
                    "capabilities": list(capabilities),
                }
            )
        return result

    def status(self, target: str) -> dict:
        return self._client(target).session()

    def list(self, target: str, path: str = ".") -> list[dict]:
        return self._client(target).list(path)

    def read(self, target: str, path: str) -> str:
        return self._client(target).read(path)

    def exec(
        self,
        target: str,
        argv: list[str],
        *,
        cwd: str = ".",
        timeout: int = 30,
    ) -> dict:
        return self._client(target).exec(argv, cwd=cwd, timeout=timeout)
