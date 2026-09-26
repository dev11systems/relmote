from __future__ import annotations

import os
import shutil
from dataclasses import dataclass


@dataclass(frozen=True)
class ScreenBackendStatus:
    session_type: str
    portal_available: bool
    pipewire_available: bool
    x11_display_available: bool
    observe_implemented: bool
    control_implemented: bool
    note: str


def detect_linux_screen_backend() -> ScreenBackendStatus:
    session_type = os.environ.get("XDG_SESSION_TYPE", "unknown").lower()
    portal = shutil.which("xdg-desktop-portal") is not None
    pipewire = shutil.which("pipewire") is not None
    x11 = bool(os.environ.get("DISPLAY"))

    if session_type == "wayland":
        note = (
            "Wayland detected. Relmote should use desktop consent/portal and "
            "PipeWire-compatible capture where available."
        )
    elif session_type == "x11" or x11:
        note = "X11 session detected. X11 screen adapter is not implemented yet."
    else:
        note = "No supported graphical-session backend has been selected yet."

    return ScreenBackendStatus(
        session_type=session_type,
        portal_available=portal,
        pipewire_available=pipewire,
        x11_display_available=x11,
        observe_implemented=False,
        control_implemented=False,
        note=note,
    )
