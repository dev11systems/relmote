from __future__ import annotations

from dataclasses import dataclass
from threading import Thread

from .agent_server import serve_agent_api
from .runtime import RelmoteRuntime


@dataclass
class RelmoteServices:
    runtime: RelmoteRuntime
    agent_host: str = "127.0.0.1"
    agent_port: int = 8788
    _agent_thread: Thread | None = None

    @classmethod
    def create(cls) -> "RelmoteServices":
        return cls(runtime=RelmoteRuntime())

    def start_agent_api(self) -> None:
        if self._agent_thread and self._agent_thread.is_alive():
            return
        self._agent_thread = Thread(
            target=serve_agent_api,
            args=(self.runtime, self.agent_host, self.agent_port),
            daemon=True,
            name="relmote-agent-api",
        )
        self._agent_thread.start()

    def snapshot(self) -> dict:
        return {
            "agent_api": {
                "host": self.agent_host,
                "port": self.agent_port,
                "running": bool(
                    self._agent_thread and self._agent_thread.is_alive()
                ),
            }
        }
