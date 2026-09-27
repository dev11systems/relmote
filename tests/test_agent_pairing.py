import pytest

from relmote.agent_controller import approve, create_request
from relmote.runtime import RelmoteRuntime


def active_grant(tmp_path):
    runtime = RelmoteRuntime()
    runtime.enable_support_until_disabled()
    pending = create_request(
        runtime,
        {
            "workspace": str(tmp_path),
            "capabilities": ["workspace.read"],
        },
    )
    approved = approve(runtime, pending["session_id"])
    return runtime, pending["session_id"], approved


def test_pairing_code_is_single_use(tmp_path):
    runtime, session_id, approved = active_grant(tmp_path)
    code = runtime.create_agent_pairing(session_id)

    exchanged = runtime.exchange_agent_pairing(code)
    assert exchanged["token"] == approved["token"]

    with pytest.raises(PermissionError):
        runtime.exchange_agent_pairing(code)


def test_pairing_fails_after_session_revocation(tmp_path):
    runtime, session_id, _ = active_grant(tmp_path)
    code = runtime.create_agent_pairing(session_id)
    runtime.revoke_agent(session_id)

    with pytest.raises(PermissionError, match="no longer active"):
        runtime.exchange_agent_pairing(code)


def test_pairing_requires_active_grant(tmp_path):
    runtime = RelmoteRuntime()
    runtime.enable_support_until_disabled()
    pending = create_request(runtime, {"workspace": str(tmp_path)})

    with pytest.raises(PermissionError, match="must be active"):
        runtime.create_agent_pairing(pending["session_id"])
