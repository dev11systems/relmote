from __future__ import annotations

import os
import pty
import select
import signal
from dataclasses import dataclass

from .terminal import TerminalAuthority, TerminalSession, TerminalState


@dataclass
class SSHTerminalProcess:
    session: TerminalSession
    pid: int
    fd: int

    def read(self, size: int = 4096, timeout: float = 0.0) -> bytes:
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

    def resize(self, rows: int, cols: int) -> None:
        if rows <= 0 or cols <= 0:
            raise ValueError("terminal dimensions must be positive")
        import fcntl
        import struct
        import termios

        fcntl.ioctl(
            self.fd,
            termios.TIOCSWINSZ,
            struct.pack("HHHH", rows, cols, 0, 0),
        )

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


class SSHTerminalBackend:
    """Interactive SSH PTY backend.

    The backend never escalates privileges itself. ADMIN authority is modeled
    separately and intentionally not implemented by this preview backend.
    """

    def open(self, session: TerminalSession) -> SSHTerminalProcess:
        if session.state is not TerminalState.ACTIVE:
            raise PermissionError("terminal request must be approved first")
        if session.authority is TerminalAuthority.ADMIN:
            raise NotImplementedError(
                "administrative terminal is not implemented in the preview"
            )

        pid, fd = pty.fork()
        if pid == 0:
            os.execvp(
                "ssh",
                [
                    "ssh",
                    "-tt",
                    "-o", "BatchMode=yes",
                    session.target,
                ],
            )
            raise SystemExit(127)

        return SSHTerminalProcess(session=session, pid=pid, fd=fd)
