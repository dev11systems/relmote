from unittest.mock import Mock, patch

import pytest

from relmote.agent_server import start_tailscale_agent_api
from relmote.runtime import RelmoteRuntime


def test_tailscale_agent_listener_requires_local_tailscale_address():
    runtime = RelmoteRuntime()
    with patch("relmote.agent_server.tailscale_ipv4", return_value=None):
        with pytest.raises(RuntimeError, match="no IPv4 address"):
            start_tailscale_agent_api(runtime)


def test_tailscale_agent_listener_binds_only_to_detected_tailscale_address():
    runtime = RelmoteRuntime()
    server = Mock()
    thread = Mock()
    thread.is_alive.return_value = True

    with patch(
        "relmote.agent_server.tailscale_ipv4",
        return_value="100.64.1.2",
    ), patch(
        "relmote.agent_server.ThreadingHTTPServer",
        return_value=server,
    ) as server_type, patch(
        "relmote.agent_server.Thread",
        return_value=thread,
    ):
        listener = start_tailscale_agent_api(runtime, 8788)

    bind = server_type.call_args.args[0]
    assert bind == ("100.64.1.2", 8788)
    assert bind[0] != "0.0.0.0"
    assert listener.host == "100.64.1.2"
    thread.start.assert_called_once_with()
