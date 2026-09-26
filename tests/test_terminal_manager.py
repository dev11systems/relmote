from dataclasses import dataclass

from relmote.terminal import TerminalSession
from relmote.terminal_manager import TerminalManager


@dataclass
class FakeProcess:
    session: TerminalSession
    written: bytes = b""
    closed: bool = False

    def read(self):
        return b"hello"

    def write(self, data):
        self.written += data

    def close(self):
        self.closed = True
        self.session.end()


class FakeBackend:
    def __init__(self):
        self.process = None

    def open(self, session):
        self.process = FakeProcess(session)
        return self.process


def test_manager_attaches_only_after_active_session():
    backend = FakeBackend()
    manager = TerminalManager(backend=backend)
    session = TerminalSession("this-computer")
    session.approve()

    manager.attach(session)

    assert manager.read(session.session_id) == b"hello"
    manager.write(session.session_id, b"ls\n")
    assert backend.process.written == b"ls\n"


def test_manager_close_ends_session():
    backend = FakeBackend()
    manager = TerminalManager(backend=backend)
    session = TerminalSession("this-computer")
    session.approve()
    manager.attach(session)

    manager.close(session.session_id)

    assert backend.process.closed
    assert session.state.value == "ended"
