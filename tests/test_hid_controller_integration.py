from io import BytesIO

from relmote.controller import RelmoteController
from relmote.model import Action, Grant, Mode
from relmote.safety import SafetyGate
from relmote.session import Session
from relmote.transports.linux_hid import LinuxHIDKeyboardTransport


def make_action(action_id: str) -> Action:
    return Action(
        "type_text",
        {"text": "hi"},
        ("input.keyboard",),
        action_id=action_id,
    )


def make_session(mode: Mode = Mode.ASSIST) -> Session:
    return Session(
        controller_id="bench-controller",
        grant=Grant(
            capabilities=frozenset({"input.keyboard"}),
            target_id="sacrificial-host",
            mode=mode,
        ),
    )


def make_gate(armed: bool) -> SafetyGate:
    gate = SafetyGate(clock=lambda: 100.0)
    if armed:
        assert gate.arm_for(15)
    return gate


def test_approved_assist_action_still_cannot_bypass_disarmed_gate():
    sink = BytesIO()
    gate = make_gate(False)
    controller = RelmoteController(
        LinuxHIDKeyboardTransport(gate, device=sink, key_delay=0)
    )
    session = make_session()
    action = make_action("integration-disarmed")

    assert controller.approve(session, action.action_id)
    outcome = controller.execute(session, action)

    assert outcome.executed is True
    assert outcome.result["completed"] is False
    assert outcome.result["stopped_by"] == "safety_gate"
    assert sink.getvalue() == b""

    # Dispatch attempts are consumed even when the hardware gate refuses them;
    # retry requires a new proposal/action ID rather than an automatic replay.
    gate.arm_for(15)
    replay = controller.execute(session, action)
    assert replay.executed is False
    assert replay.reason == "action already executed"
    assert sink.getvalue() == b""


def test_armed_gate_and_explicit_approval_reach_hid_sink_once():
    sink = BytesIO()
    gate = make_gate(True)
    controller = RelmoteController(
        LinuxHIDKeyboardTransport(gate, device=sink, key_delay=0)
    )
    session = make_session()
    action = make_action("integration-success")

    waiting = controller.execute(session, action)
    assert waiting.executed is False
    assert waiting.status == "approval_required"
    assert sink.getvalue() == b""

    assert controller.approve(session, action.action_id)
    outcome = controller.execute(session, action)

    assert outcome.executed is True
    assert outcome.result["completed"] is True
    assert outcome.result["characters_sent"] == 2
    assert len(sink.getvalue()) == 32

    replay = controller.execute(session, action)
    assert replay.executed is False
    assert len(sink.getvalue()) == 32


def test_operate_mode_still_requires_physical_gate():
    sink = BytesIO()
    gate = make_gate(False)
    controller = RelmoteController(
        LinuxHIDKeyboardTransport(gate, device=sink, key_delay=0)
    )
    session = make_session(Mode.OPERATE)
    action = make_action("operate-disarmed")

    outcome = controller.execute(session, action)

    assert outcome.executed is True
    assert outcome.result["completed"] is False
    assert outcome.result["stopped_by"] == "safety_gate"
    assert sink.getvalue() == b""
