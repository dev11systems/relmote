from __future__ import annotations

import os
import shutil
import subprocess
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


def _loginctl_graphical_session_type() -> str | None:
    if shutil.which("loginctl") is None:
        return None
    user = os.environ.get("USER")
    try:
        listed = subprocess.run(
            ["loginctl", "list-sessions", "--no-legend"],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if listed.returncode != 0:
        return None

    for raw in listed.stdout.splitlines():
        fields = raw.split()
        if not fields:
            continue
        session_id = fields[0]
        try:
            shown = subprocess.run(
                ["loginctl", "show-session", session_id,
                 "-p", "Name", "-p", "Type", "-p", "Class", "-p", "Active"],
                capture_output=True,
                text=True,
                timeout=3,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            continue
        props = {}
        for line in shown.stdout.splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                props[key] = value
        if user and props.get("Name") != user:
            continue
        if props.get("Type") in {"wayland", "x11"} and props.get("Class") == "user":
            return props["Type"]
    return None


def detect_linux_screen_backend() -> ScreenBackendStatus:
    session_type = os.environ.get("XDG_SESSION_TYPE", "").lower()
    if session_type not in {"wayland", "x11"}:
        session_type = _loginctl_graphical_session_type() or "unknown"

    portal = shutil.which("xdg-desktop-portal") is not None
    pipewire = shutil.which("pipewire") is not None
    x11 = bool(os.environ.get("DISPLAY"))

    if session_type == "wayland":
        note = (
            "Wayland graphical session detected. Screen observation/control "
            "backend is not implemented yet."
        )
    elif session_type == "x11" or x11:
        note = "X11 graphical session detected. X11 screen adapter is not implemented yet."
    else:
        note = "No supported graphical session was detected."

    return ScreenBackendStatus(
        session_type=session_type,
        portal_available=portal,
        pipewire_available=pipewire,
        x11_display_available=x11,
        observe_implemented=False,
        control_implemented=False,
        note=note,
    )
