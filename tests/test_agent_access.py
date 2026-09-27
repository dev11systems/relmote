from unittest.mock import Mock, patch

import pytest

from relmote.agent_access import (
    direct_transport_status,
    disable_direct_transport,
    enable_direct_transport,
)
from relmote.runtime import RelmoteRuntime


def test_direct_transport_status_reports_tailscale_endpoint():
    runtime = RelmoteRuntime()
    listener = Mock()
    listener.running = True
    listener.host = "100.64.1.2"
    listener.port = 8788
    runtime._agent_direct_listener = listener

    with patch(
        "relmote.agent_access.tailscale_ipv4",
        return_value="100.64.1.2",
    ):
        status = direct_transport_status(runtime)

    assert status["enabled"] is True
    assert status["kind"] == "tailscale-direct"
    assert status["url"] == "http://100.64.1.2:8788"


def test_enable_direct_transport_requires_tailscale_address():
    runtime = RelmoteRuntime()

    with patch("relmote.agent_access.tailscale_ipv4", return_value=None):
        with pytest.raises(RuntimeError, match="no IPv4 address"):
            enable_direct_transport(runtime)


def test_enable_direct_transport_starts_listener():
    runtime = RelmoteRuntime()
    listener = Mock()
    listener.running = True
    listener.host = "100.64.1.2"
    listener.port = 8788

    with patch(
        "relmote.agent_access.tailscale_ipv4",
        return_value="100.64.1.2",
    ), patch(
        "relmote.agent_access.start_tailscale_agent_api",
        return_value=listener,
    ) as start:
        status = enable_direct_transport(runtime)

    start.assert_called_once_with(runtime, 8788)
    assert runtime._agent_direct_listener is listener
    assert status["url"] == "http://100.64.1.2:8788"


def test_disable_direct_transport_stops_listener():
    runtime = RelmoteRuntime()
    listener = Mock()
    listener.running = True
    listener.host = "100.64.1.2"
    listener.port = 8788
    runtime._agent_direct_listener = listener

    with patch(
        "relmote.agent_access.tailscale_ipv4",
        return_value="100.64.1.2",
    ):
        status = disable_direct_transport(runtime)

    listener.stop.assert_called_once_with()
    assert runtime._agent_direct_listener is None
    assert status["enabled"] is False
