import pytest

from relmote.safety_protocol import ReplayWindow, SafetyCommand, SafetyMessage


def message(sequence=1, text="hello"):
    return SafetyMessage(
        command=SafetyCommand.TYPE_TEXT,
        message_id=f"m-{sequence}",
        session_id="session-1",
        lease_id="lease-1",
        sequence=sequence,
        payload={"text": text},
    )


def test_valid_type_text():
    message().validate()


def test_type_text_requires_lease():
    value = SafetyMessage(
        command=SafetyCommand.TYPE_TEXT,
        message_id="m-1",
        session_id="session-1",
        lease_id=None,
        sequence=1,
        payload={"text": "hello"},
    )

    with pytest.raises(ValueError, match="lease_id"):
        value.validate()


def test_safety_plane_has_smaller_text_bound():
    with pytest.raises(ValueError, match="128"):
        message(text="a" * 129).validate()


def test_replay_window_rejects_same_or_older_sequence():
    window = ReplayWindow()

    assert window.accept(10)
    assert not window.accept(10)
    assert not window.accept(9)
    assert window.accept(11)
