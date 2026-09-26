import pytest

from relmote.ssh_terminal import SSHTerminalBackend
from relmote.terminal import TerminalAuthority, TerminalSession


def test_backend_refuses_unapproved_terminal():
    with pytest.raises(PermissionError):
        SSHTerminalBackend().open(TerminalSession("target-host"))


def test_backend_refuses_admin_preview_before_spawning():
    session = TerminalSession(
        "target-host",
        authority=TerminalAuthority.ADMIN,
    )
    session.approve()

    with pytest.raises(NotImplementedError, match="administrative"):
        SSHTerminalBackend().open(session)
