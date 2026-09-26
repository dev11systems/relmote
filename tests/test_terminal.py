import pytest

from relmote.terminal import (
    TerminalAuthority,
    TerminalSession,
    TerminalState,
)


def test_terminal_requires_explicit_approval():
    session = TerminalSession("target-host")

    assert session.requires_approval
    assert session.state is TerminalState.REQUESTED

    session.approve()
    assert session.state is TerminalState.ACTIVE

    session.end()
    assert session.state is TerminalState.ENDED


def test_admin_is_distinct_authority():
    session = TerminalSession(
        "target-host",
        authority=TerminalAuthority.ADMIN,
    )
    assert session.authority is TerminalAuthority.ADMIN


def test_invalid_state_transition_is_rejected():
    session = TerminalSession("target-host")
    with pytest.raises(ValueError):
        session.end()
