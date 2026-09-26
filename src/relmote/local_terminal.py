from __future__ import annotations

import os
import pty
import pwd
import select
import signal
from dataclasses import dataclass

from .terminal import TerminalAuthority, TerminalSession, TerminalState


@dataclass
class LocalTerminalProcess:
    session: TerminalSession
    pid: int
    fd: int

    def read(self, size: int = 16384, timeout: float = 0.0) -> bytes:
        readable, _, _ = select.select([self.fd], [], [], timeout)
        if not readable:
            return b""
        try:
            return os.read(self.fd, size)
        except OSError:
            return b""

    def write(self, data: bytes) -> int:
        if self.session.state is not TerminalState.ACTIVE:
            raise PermissionError("terminal session is not active")
        return os.write(self.fd, data)

    def close(self) -> None:
        if self.session.state is TerminalState.ACTIVE:
            self.session.end()
        try:
            os.close(self.fd)
        except OSError:
            pass
        try:
            os.kill(self.pid, signal.SIGHUP)
        except OSError:
            pass


class LocalTerminalBackend:
    """Normal-user local PTY for an approved Relmote terminal session."""

    def open(self, session: TerminalSession) -> LocalTerminalProcess:
        if session.state is not TerminalState.ACTIVE:
            raise PermissionError("terminal request must be approved first")
        if session.authority is TerminalAuthority.ADMIN:
            raise NotImplementedError(
                "administrative terminal is not implemented in the preview"
            )

        shell = os.environ.get("SHELL") or pwd.getpwuid(os.getuid()).pw_shell or "/bin/sh"
        pid, fd = pty.fork()
        if pid == 0:
            os.execv(shell, [shell, "-l"])
            raise SystemExit(127)
        return LocalTerminalProcess(session=session, pid=pid, fd=fd)
