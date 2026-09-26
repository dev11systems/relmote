from io import BytesIO

import pytest

from relmote.model import Action
from relmote.transports.linux_hid import (
    EMPTY_REPORT,
    LEFT_SHIFT,
    LinuxHIDKeyboardTransport,
    keyboard_report,
)


def action(text: str, action_id: str = "hid-1") -> Action:
    return Action(
        "type_text",
        {"text": text},
        ("input.keyboard",),
        action_id=action_id,
    )


def test_encodes_lowercase_and_release():
    sink = BytesIO()
    transport = LinuxHIDKeyboardTransport(device=sink, key_delay=0)

    result = transport.execute(action("a"))

    assert result["completed"] is True
    assert sink.getvalue() == bytes((0, 0, 0x04, 0, 0, 0, 0, 0)) + EMPTY_REPORT


def test_uppercase_uses_shift():
    report = keyboard_report("A")
    assert report[0] == LEFT_SHIFT
    assert report[2] == 0x04


def test_validates_entire_string_before_output():
    sink = BytesIO()
    transport = LinuxHIDKeyboardTransport(device=sink, key_delay=0)

    with pytest.raises(ValueError):
        transport.execute(action("ok🙂"))

    assert sink.getvalue() == b""


def test_rejects_non_text_action():
    sink = BytesIO()
    transport = LinuxHIDKeyboardTransport(device=sink, key_delay=0)
    bad = Action("raw_report", {"bytes": [1, 2]}, ("input.keyboard",))

    with pytest.raises(ValueError):
        transport.execute(bad)

    assert sink.getvalue() == b""


def test_rejects_extra_capabilities():
    sink = BytesIO()
    transport = LinuxHIDKeyboardTransport(device=sink, key_delay=0)
    bad = Action(
        "type_text",
        {"text": "hello"},
        ("input.keyboard", "shell.write"),
    )

    with pytest.raises(ValueError):
        transport.execute(bad)


def test_text_length_limit_fails_before_output():
    sink = BytesIO()
    transport = LinuxHIDKeyboardTransport(
        device=sink,
        key_delay=0,
        max_text_length=4,
    )

    with pytest.raises(ValueError):
        transport.execute(action("hello"))

    assert sink.getvalue() == b""


def test_stop_predicate_interrupts_between_characters():
    sink = BytesIO()
    checks = iter([False, True])
    transport = LinuxHIDKeyboardTransport(
        device=sink,
        key_delay=0,
        stop_requested=lambda: next(checks),
    )

    result = transport.execute(action("ab"))

    assert result["completed"] is False
    assert result["interrupted"] is True
    assert result["characters_sent"] == 1
    # a press, release, then an extra release when STOP is observed
    assert len(sink.getvalue()) == 24
