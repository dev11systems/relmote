from datetime import timedelta

from relmote.audit import AuditLog
from relmote.controller import RelmoteController
from relmote.model import Action, Grant, Mode
from relmote.session import Session, utcnow
from relmote.transports.dry_run import DryRunTransport


def make_session(mode=Mode.ASSIST, *, expires_at=None):
    return Session(
        controller_id="tester",
        grant=Grant(
            capabilities=frozenset({"input.keyboard"}),
            target_id="test-host",
            mode=mode,
            expires_at=expires_at,
        ),
    )


def make_action(action_id="action-1"):
    return Action(
        "type_text",
        {"text": "hello"},
        ("input.keyboard",),
        action_id=action_id,
    )


def test_assist_requires_exact_action_approval():
    controller = RelmoteController(DryRunTransport())
    session = make_session()
    action = make_action()

    first = controller.execute(session, action)
    assert not first.executed
    assert first.status == "approval_required"

    assert controller.approve(session, action.action_id)
    second = controller.execute(session, action)
    assert second.executed
    assert second.result["simulated"] is True


def test_action_id_cannot_execute_twice():
    controller = RelmoteController(DryRunTransport())
    session = make_session(Mode.OPERATE)
    action = make_action()

    assert controller.execute(session, action).executed
    replay = controller.execute(session, action)
    assert not replay.executed
    assert replay.reason == "action already executed"


def test_revocation_stops_future_output_and_clears_approval():
    controller = RelmoteController(DryRunTransport())
    session = make_session()
    action = make_action()

    assert controller.approve(session, action.action_id)
    controller.revoke(session)

    outcome = controller.execute(session, action)
    assert not outcome.executed
    assert outcome.reason == "session revoked"
    assert not session.is_approved(action.action_id)


def test_expired_session_fails_closed():
    controller = RelmoteController(DryRunTransport())
    session = make_session(expires_at=utcnow() - timedelta(seconds=1))

    outcome = controller.execute(session, make_action())
    assert not outcome.executed
    assert outcome.reason == "session expired"


def test_audit_does_not_log_payload_by_default():
    audit = AuditLog()
    controller = RelmoteController(DryRunTransport(), audit)
    session = make_session(Mode.OPERATE)
    action = Action(
        "type_text",
        {"text": "SECRET SHOULD NOT ENTER AUDIT"},
        ("input.keyboard",),
        action_id="private-action",
    )

    assert controller.execute(session, action).executed
    assert "SECRET SHOULD NOT ENTER AUDIT" not in audit.to_jsonl()
