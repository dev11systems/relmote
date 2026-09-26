import pytest

from relmote.local_terminal import LocalTerminalBackend
from relmote.terminal import TerminalAuthority, TerminalSession


def test_local_terminal_refuses_unapproved_session():
    with pytest.raises(PermissionError):
        LocalTerminalBackend().open(TerminalSession("this-computer"))


def test_local_terminal_refuses_admin_before_spawn():
    session = TerminalSession(
        "this-computer",
        authority=TerminalAuthority.ADMIN,
    )
    session.approve()

    with pytest.raises(NotImplementedError, match="administrative"):
        LocalTerminalBackend().open(session)
