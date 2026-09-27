from unittest.mock import patch

from relmote.agent_controller_api import handle
from relmote.runtime import RelmoteRuntime


def test_agent_access_status_endpoint_reports_transport_state():
    runtime = RelmoteRuntime()
    with patch(
        "relmote.agent_access_service.serve_status",
        return_value={
            "available": True,
            "enabled": False,
            "kind": "tailscale-serve",
        },
    ):
        status, value = handle(
            runtime,
            "/api/v1/controller/agent/status",
            {},
        )

    assert status == 200
    assert value["enabled"] is False
    assert value["transport"]["available"] is True


def test_agent_access_enable_endpoint_uses_private_transport():
    runtime = RelmoteRuntime()
    with patch(
        "relmote.agent_access_service.enable_private_transport",
        return_value={"enabled": True, "kind": "tailscale-serve"},
    ), patch(
        "relmote.agent_access_service.serve_status",
        return_value={
            "available": True,
            "enabled": True,
            "kind": "tailscale-serve",
        },
    ):
        status, value = handle(
            runtime,
            "/api/v1/controller/agent/enable",
            {},
        )

    assert status == 200
    assert value["enabled"] is True
