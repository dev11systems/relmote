from __future__ import annotations

from dataclasses import dataclass, field

from .local_terminal import LocalTerminalBackend, LocalTerminalProcess
from .terminal import TerminalSession, TerminalState


@dataclass
class TerminalManager:
    processes: dict[str, LocalTerminalProcess] = field(default_factory=dict)
    backend: LocalTerminalBackend = field(default_factory=LocalTerminalBackend)

    def attach(self, session: TerminalSession) -> None:
        if session.state is not TerminalState.ACTIVE:
            raise PermissionError("terminal session is not active")
        if session.session_id in self.processes:
            return
        self.processes[session.session_id] = self.backend.open(session)

    def read(self, session_id: str) -> bytes:
        process = self.processes.get(session_id)
        if process is None:
            raise KeyError("terminal process is not attached")
        return process.read()

    def write(self, session_id: str, data: bytes) -> None:
        process = self.processes.get(session_id)
        if process is None:
            raise KeyError("terminal process is not attached")
        process.write(data)

    def close(self, session_id: str) -> None:
        process = self.processes.pop(session_id, None)
        if process is not None:
            process.close()

    def close_all(self) -> None:
        for session_id in tuple(self.processes):
            self.close(session_id)
