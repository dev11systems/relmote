from unittest.mock import patch

from relmote.agent_api import handle_get
from relmote.runtime import RelmoteRuntime


class Headers(dict):
    pass


def active_runtime():
    runtime = RelmoteRuntime()
    runtime.support_access.enable_until_disabled()
    grant = runtime.request_agent(
        "/workspace",
        ["workspace.list"],
        controller="test-controller",
    )
    runtime.approve_agent(grant.session.session_id)
    return runtime, grant


def test_agent_info_returns_minimal_authenticated_target_metadata():
    runtime, grant = active_runtime()
    headers = Headers(Authorization=f"Bearer {grant.token}")

    with patch(
        "relmote.agent_api.platform.system",
        return_value="Linux",
    ), patch(
        "relmote.agent_api.platform.machine",
        return_value="x86_64",
    ), patch(
        "relmote.agent_api.build_info",
        return_value={
            "version": "0.1.0.dev12",
            "display_version": "0.1.0-dev.12",
            "commit": "abcdef1234567890",
            "short_commit": "abcdef12",
            "channel": "repository",
        },
    ):
        value = handle_get(runtime, headers, "/api/v1/agent/info")

    assert value["role"] == "target"
    assert value["target"]["name"] == runtime.node.identity.display_name
    assert value["platform"] == {
        "system": "linux",
        "architecture": "x86_64",
    }
    assert value["relmote"]["short_commit"] == "abcdef12"
    assert value["session"]["state"] == "active"
    assert "token" not in repr(value)
