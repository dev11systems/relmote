from __future__ import annotations

from .network_exposure import tailscale_ipv4


def tailscale_transport(port: int = 8788) -> dict:
    address = tailscale_ipv4()
    if not address:
        return {
            "available": False,
            "kind": "tailscale-direct",
            "message": "Tailscale is not connected or has no IPv4 address.",
            "address": None,
            "endpoint": None,
            "optional_serve_command": None,
        }

    return {
        "available": True,
        "kind": "tailscale-direct",
        "address": address,
        "endpoint": f"http://{address}:{port}",
        "message": (
            "Preferred Agent transport: bind the Agent API only to this "
            "machine's Tailscale address. Tailscale provides encrypted private "
            "reachability; Relmote pairing/grants remain the authorization layer."
        ),
        "optional_serve_command": f"tailscale serve --bg {port}",
        "optional_serve_status_command": "tailscale serve status",
    }
