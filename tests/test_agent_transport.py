from unittest.mock import patch

from relmote.agent_transport import tailscale_transport


def test_preferred_agent_transport_is_direct_tailscale():
    with patch(
        "relmote.agent_transport.tailscale_ipv4",
        return_value="100.64.1.2",
    ):
        value = tailscale_transport()

    assert value["available"] is True
    assert value["kind"] == "tailscale-direct"
    assert value["endpoint"] == "http://100.64.1.2:8788"
    assert value["optional_serve_command"] == "tailscale serve --bg 8788"


def test_direct_tailscale_transport_is_unavailable_without_address():
    with patch("relmote.agent_transport.tailscale_ipv4", return_value=None):
        value = tailscale_transport()

    assert value["available"] is False
    assert value["endpoint"] is None
