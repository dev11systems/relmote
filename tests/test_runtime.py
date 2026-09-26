from relmote.runtime import RelmoteRuntime


def test_frontends_share_one_runtime_state():
    runtime = RelmoteRuntime()

    assert runtime.snapshot()["session"] is None

    runtime.start_checks()
    assert runtime.snapshot()["session"]["mode"] == "observe"

    runtime.run_task("full-check")
    assert runtime.snapshot()["tasks"][-1]["task_type"] == "full-check"

    runtime.stop_checks()
    assert runtime.snapshot()["session"]["revoked"] is True


def test_runtime_has_shared_event_stream():
    runtime = RelmoteRuntime()
    runtime.start_checks()
    runtime.run_task("storage-overview")

    result = runtime.events_since()

    assert [event["kind"] for event in result["events"]] == [
        "session.started",
        "task.completed",
    ]


def test_remote_support_is_off_by_default_and_separate_from_local_checks():
    runtime = RelmoteRuntime()

    runtime.start_checks()
    snapshot = runtime.snapshot()

    assert snapshot["session"]["mode"] == "observe"
    assert snapshot["support"]["available"] is False
    assert snapshot["support"]["mode"] == "disabled"


def test_remote_support_can_be_enabled_and_disabled():
    runtime = RelmoteRuntime()

    runtime.enable_support_until_disabled()
    assert runtime.snapshot()["support"] == {
        "available": True,
        "mode": "until-disabled",
    }

    runtime.disable_support()
    assert runtime.snapshot()["support"]["available"] is False
    assert runtime.snapshot()["support"]["mode"] == "disabled"


def test_terminal_request_requires_remote_support():
    runtime = RelmoteRuntime()

    import pytest
    with pytest.raises(PermissionError, match="support is off"):
        runtime.request_terminal("target-host")


def test_terminal_request_can_be_approved_and_ended():
    runtime = RelmoteRuntime()
    runtime.enable_support_until_disabled()

    terminal = runtime.request_terminal(
        "target-host",
        controller="helper-device",
    )
    assert terminal.state.value == "requested"

    runtime.approve_terminal(terminal.session_id)
    assert terminal.state.value == "active"

    snapshot = runtime.snapshot()
    assert snapshot["terminal_sessions"][0]["controller"] == "helper-device"
    assert snapshot["terminal_sessions"][0]["authority"] == "user"

    runtime.end_terminal(terminal.session_id)
    assert terminal.state.value == "ended"
