from unittest.mock import patch

from relmote.agent_access_service import AgentAccessService
from relmote.agent_controller import approve, create_request
from relmote.runtime import RelmoteRuntime


def test_disable_revokes_active_grants_before_transport_teardown(tmp_path):
    runtime = RelmoteRuntime()
    runtime.enable_support_until_disabled()
    pending = create_request(runtime, {"workspace": str(tmp_path)})
    approve(runtime, pending["session_id"])
    service = AgentAccessService(runtime)

    with patch(
        "relmote.agent_access_service.disable_direct_transport",
        return_value={"enabled": False},
    ):
        with patch(
            "relmote.agent_access_service.direct_transport_status",
            return_value={"available": True, "enabled": False},
        ):
            status = service.disable()

    assert runtime.agent_grants[pending["session_id"]].session.state.value == "ended"
    assert status["enabled"] is False


def test_pairing_service_never_returns_bearer_token(tmp_path):
    runtime = RelmoteRuntime()
    runtime.enable_support_until_disabled()
    pending = create_request(runtime, {"workspace": str(tmp_path)})
    approve(runtime, pending["session_id"])
    service = AgentAccessService(runtime)

    paired = service.pair_session(pending["session_id"])

    assert paired["code"]
    assert "token" not in paired


def test_enable_uses_direct_tailscale_transport():
    runtime = RelmoteRuntime()
    service = AgentAccessService(runtime)

    with patch(
        "relmote.agent_access_service.enable_direct_transport",
        return_value={
            "available": True,
            "enabled": True,
            "kind": "tailscale-direct",
            "bound_address": "100.64.1.2",
            "url": "http://100.64.1.2:8788",
        },
    ), patch(
        "relmote.agent_access_service.direct_transport_status",
        return_value={
            "available": True,
            "enabled": True,
            "kind": "tailscale-direct",
            "bound_address": "100.64.1.2",
            "url": "http://100.64.1.2:8788",
        },
    ):
        status = service.enable_transport()

    assert status["enabled"] is True
    assert status["transport"]["kind"] == "tailscale-direct"
