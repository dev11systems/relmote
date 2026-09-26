from relmote.api import LocalControllerAPI
from relmote.events import Event, EventStream
from relmote.node_state import NodeState
from relmote.routing import TaskRequirements
from relmote.topology import Feedback, Node, Path, Target, TargetPath


def api():
    node = Node(
        node_id="rm:test",
        name="Pocket",
        controller_paths=(
            Path("ble", "ble", interactive=True, authenticated=True),
        ),
    )
    target = Target(
        target_id="target:test",
        name="ThinkPad",
        system_paths=(
            TargetPath(
                "hid",
                "usb.hid",
                Feedback.NONE,
                works_before_os=True,
            ),
        ),
    )
    state = NodeState(node=node, targets={target.target_id: target})
    return LocalControllerAPI(state, EventStream())


def test_snapshot_exposes_path_and_feedback():
    value = api().snapshot()

    assert value["node"]["reachability"] == "online-interactive"
    assert value["targets"][0]["system_paths"][0]["feedback"] == "none"


def test_api_route_preserves_blind_hid_warning():
    result = api().route_task(
        "target:test",
        TaskRequirements(needs_input=True),
    )

    assert result.usable
    assert "no target feedback" in result.limitations


def test_unknown_target_fails_cleanly():
    result = api().route_task("missing", TaskRequirements())

    assert not result.usable
    assert result.reason == "unknown target"


def test_event_stream_is_semantic():
    value = api()
    value.events.publish(
        Event(
            "physical.stop_latched",
            node_id="rm:test",
            target_id="target:test",
        )
    )

    events = value.event_snapshot()
    assert events[0]["event_type"] == "physical.stop_latched"
