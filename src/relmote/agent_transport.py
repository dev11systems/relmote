from __future__ import annotations

import shutil


def tailscale_transport(port: int = 8788) -> dict:
    tailscale = shutil.which("tailscale")
    if not tailscale:
        return {
            "available": False,
            "kind": "tailscale-serve",
            "message": "Tailscale CLI was not found.",
            "command": None,
        }

    return {
        "available": True,
        "kind": "tailscale-serve",
        "message": (
            "Expose the loopback-only Agent API privately to this tailnet. "
            "This does not use Funnel and does not make the API public."
        ),
        "command": f"tailscale serve --bg {port}",
        "status_command": "tailscale serve status",
        "disable_command": "tailscale serve reset",
    }
