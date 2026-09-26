from io import BytesIO

import pytest

from relmote.model import Action
from relmote.safety import SafetyGate
from relmote.transports.base import ExecutionContext
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


def context(should_stop=lambda: False) -> ExecutionContext:
    return ExecutionContext(
        session_id="session-1",
        target_id="test-host",
        should_stop=should_stop,
    )


def armed_gate() -> SafetyGate:
    gate = SafetyGate(clock=lambda: 100.0)
    assert gate.arm_for(60)
    return gate


def test_disarmed_gate_emits_nothing():
    sink = BytesIO()
    gate = SafetyGate(clock=lambda: 100.0)
    transport = LinuxHIDKeyboardTransport(gate, device=sink, key_delay=0)

    result = transport.execute(action("a"), context())

    assert result["completed"] is False
    assert result["stopped_by"] == "safety_gate"
    assert sink.getvalue() == b""


def test_encodes_lowercase_and_release_when_armed():
    sink = BytesIO()
    transport = LinuxHIDKeyboardTransport(
        armed_gate(),
        device=sink,
        key_delay=0,
    )

    result = transport.execute(action("a"), context())

    assert result["completed"] is True
    assert sink.getvalue() == bytes((0, 0, 0x04, 0, 0, 0, 0, 0)) + EMPTY_REPORT


def test_uppercase_uses_shift():
    report = keyboard_report("A")
    assert report[0] == LEFT_SHIFT
    assert report[2] == 0x04


def test_validates_entire_string_before_output():
    sink = BytesIO()
    transport = LinuxHIDKeyboardTransport(
        armed_gate(),
        device=sink,
        key_delay=0,
    )

    with pytest.raises(ValueError):
        transport.execute(action("ok🙂"), context())

    assert sink.getvalue() == b""


def test_rejects_non_text_action():
    sink = BytesIO()
    transport = LinuxHIDKeyboardTransport(
        armed_gate(),
        device=sink,
        key_delay=0,
    )
    bad = Action("raw_report", {"bytes": [1, 2]}, ("input.keyboard",))

    with pytest.raises(ValueError):
        transport.execute(bad, context())

    assert sink.getvalue() == b""


def test_rejects_extra_capabilities():
    sink = BytesIO()
    transport = LinuxHIDKeyboardTransport(
        armed_gate(),
        device=sink,
        key_delay=0,
    )
    bad = Action(
        "type_text",
        {"text": "hello"},
        ("input.keyboard", "shell.write"),
    )

    with pytest.raises(ValueError):
        transport.execute(bad, context())


def test_text_length_limit_fails_before_output():
    sink = BytesIO()
    transport = LinuxHIDKeyboardTransport(
        armed_gate(),
        device=sink,
        key_delay=0,
        max_text_length=4,
    )

    with pytest.raises(ValueError):
        transport.execute(action("hello"), context())

    assert sink.getvalue() == b""


def test_latched_gate_stop_interrupts_between_characters():
    sink = BytesIO()

    class SequencedGate:
        def __init__(self):
            self.checks = iter([False, False, True])

        def permits_output(self):
            return True

        def stop_requested(self):
            return next(self.checks)

    transport = LinuxHIDKeyboardTransport(
        SequencedGate(),
        device=sink,
        key_delay=0,
    )

    result = transport.execute(action("ab"), context())

    assert result["completed"] is False
    assert result["interrupted"] is True
    assert result["stopped_by"] == "safety_gate"
    assert result["characters_sent"] == 1
    # a press, release, then an extra release when STOP is observed
    assert len(sink.getvalue()) == 24


def test_live_session_cancellation_interrupts_between_characters():
    sink = BytesIO()
    checks = iter([False, False, True])
    transport = LinuxHIDKeyboardTransport(
        armed_gate(),
        device=sink,
        key_delay=0,
    )

    result = transport.execute(
        action("ab"),
        context(should_stop=lambda: next(checks)),
    )

    assert result["completed"] is False
    assert result["stopped_by"] == "session"
    assert result["characters_sent"] == 1
    assert len(sink.getvalue()) == 24


def test_activity_callback_wraps_real_device_output():
    sink = BytesIO()
    states = []
    transport = LinuxHIDKeyboardTransport(
        armed_gate(),
        device=sink,
        key_delay=0,
        activity_changed=states.append,
    )

    result = transport.execute(action("a"), context())

    assert result["completed"] is True
    assert states == [True, False]


def test_disarmed_transport_never_sets_activity():
    sink = BytesIO()
    states = []
    gate = SafetyGate(clock=lambda: 100.0)
    transport = LinuxHIDKeyboardTransport(
        gate,
        device=sink,
        key_delay=0,
        activity_changed=states.append,
    )

    transport.execute(action("a"), context())

    assert states == []
