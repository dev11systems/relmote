from relmote.agent_controller import approve, create_request
from relmote.runtime import RelmoteRuntime


def test_agent_token_only_revealed_by_approval(tmp_path):
    runtime = RelmoteRuntime()
    runtime.enable_support_until_disabled()

    pending = create_request(
        runtime,
        {
            "workspace": str(tmp_path),
            "capabilities": ["workspace.list", "workspace.read"],
        },
    )

    assert pending["state"] == "requested"
    assert "token" not in pending

    approved = approve(runtime, pending["session_id"])
    assert approved["state"] == "active"
    assert approved["token"]

    snapshot = runtime.snapshot()
    public = next(
        item for item in snapshot["agent_sessions"]
        if item["session_id"] == pending["session_id"]
    )
    assert public["state"] == "active"
    assert "token" not in public


def test_disabling_support_revokes_agent(tmp_path):
    runtime = RelmoteRuntime()
    runtime.enable_support_until_disabled()
    pending = create_request(runtime, {"workspace": str(tmp_path)})
    approve(runtime, pending["session_id"])

    runtime.disable_support()

    assert runtime.agent_grants[pending["session_id"]].session.state.value == "ended"


def test_revoked_bearer_token_is_rejected(tmp_path):
    runtime = RelmoteRuntime()
    runtime.enable_support_until_disabled()
    pending = create_request(runtime, {"workspace": str(tmp_path)})
    approved = approve(runtime, pending["session_id"])

    runtime.revoke_agent(pending["session_id"])

    import pytest
    with pytest.raises(PermissionError, match="not active"):
        runtime.agent_by_token(approved["token"])
