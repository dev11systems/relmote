from __future__ import annotations

import shutil

from .screen_backend import detect_linux_screen_backend
from .wayland_portal import portal_screen_cast_available
from .screen_providers import discover_screen_providers, preferred_observe_provider


def remote_feature_status() -> dict[str, dict]:
    screen = detect_linux_screen_backend()
    ssh = shutil.which("ssh") is not None
    portal_ready, portal_note = (
        portal_screen_cast_available()
        if screen.session_type == "wayland"
        else (False, "ScreenCast portal check applies to Wayland sessions.")
    )

    return {
        "screen": {
            "available": screen.observe_implemented,
            "control_available": screen.control_implemented,
            "session_type": screen.session_type,
            "portal_ready": portal_ready,
            "portal_note": portal_note,
            "note": screen.note,
            "providers": [item.as_dict() for item in discover_screen_providers()],
            "preferred_observe_provider": (
                preferred_observe_provider().provider_id
                if preferred_observe_provider() else None
            ),
        },
        "terminal": {
            "available": ssh,
            "interactive_web_implemented": True,
            "transport": "ssh" if ssh else None,
            "note": (
                "Interactive normal-user browser terminal is available."
                if ssh
                else "Local browser terminal is available; SSH target transport is not installed."
            ),
        },
    }
