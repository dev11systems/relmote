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
