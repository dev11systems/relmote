from relmote.model import Action, Grant, Mode
from relmote.policy import evaluate


def test_teach_mode_never_executes():
    grant = Grant(
        capabilities=frozenset({"input.keyboard"}),
        target_id="test-host",
        mode=Mode.TEACH,
    )
    decision = evaluate(
        Action("type_text", {"text": "hello"}, ("input.keyboard",)),
        grant,
    )
    assert not decision.allowed


def test_assist_requires_approval():
    grant = Grant(
        capabilities=frozenset({"input.keyboard"}),
        target_id="test-host",
        mode=Mode.ASSIST,
    )
    decision = evaluate(
        Action("type_text", {"text": "hello"}, ("input.keyboard",)),
        grant,
    )
    assert decision.allowed
    assert decision.requires_approval


def test_missing_capability_fails_closed():
    grant = Grant(
        capabilities=frozenset(),
        target_id="test-host",
        mode=Mode.OPERATE,
    )
    decision = evaluate(
        Action("type_text", {"text": "hello"}, ("input.keyboard",)),
        grant,
    )
    assert not decision.allowed
