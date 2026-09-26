from __future__ import annotations

import shutil

from .screen_backend import detect_linux_screen_backend


def remote_feature_status() -> dict[str, dict]:
    screen = detect_linux_screen_backend()
    ssh = shutil.which("ssh") is not None

    return {
        "screen": {
            "available": screen.observe_implemented,
            "control_available": screen.control_implemented,
            "session_type": screen.session_type,
            "note": screen.note,
        },
        "terminal": {
            "available": ssh,
            "interactive_web_implemented": False,
            "transport": "ssh" if ssh else None,
            "note": (
                "SSH transport is available; interactive browser terminal is not implemented yet."
                if ssh
                else "SSH client not found."
            ),
        },
    }
