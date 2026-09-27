from __future__ import annotations

import os
import shutil
from dataclasses import dataclass, asdict

from .screen_backend import detect_linux_screen_backend
from .wayland_portal import portal_screen_cast_available


@dataclass(frozen=True)
class ScreenProvider:
    provider_id: str
    label: str
    available: bool
    observe: bool
    control: bool
    consent: str
    scope: str
    note: str

    def as_dict(self) -> dict:
        return asdict(self)


def discover_screen_providers() -> tuple[ScreenProvider, ...]:
    screen = detect_linux_screen_backend()
    portal_ready, portal_note = (
        portal_screen_cast_available()
        if screen.session_type == "wayland"
        else (False, "Wayland session not detected.")
    )

    providers = [
        ScreenProvider(
            "wayland-portal",
            "Wayland portal / PipeWire",
            portal_ready,
            portal_ready,
            False,
            "os-mediated",
            "logged-in-session",
            portal_note,
        ),
        ScreenProvider(
            "gnome-rdp",
            "GNOME Remote Desktop / RDP",
            shutil.which("grdctl") is not None,
            shutil.which("grdctl") is not None,
            shutil.which("grdctl") is not None,
            "gnome-configured",
            "desktop-session",
            (
                "GNOME Remote Desktop tooling detected."
                if shutil.which("grdctl")
                else "GNOME Remote Desktop tooling not detected."
            ),
        ),
        ScreenProvider(
            "vnc",
            "VNC",
            any(shutil.which(name) for name in ("wayvnc", "x11vnc", "tigervncserver", "vncserver")),
            True,
            True,
            "provider-configured",
            "desktop-session",
            "Existing VNC tooling may be used when explicitly configured.",
        ),
        ScreenProvider(
            "x11-native",
            "X11 native",
            screen.session_type == "x11" or bool(os.environ.get("DISPLAY")),
            True,
            True,
            "session-policy",
            "desktop-session",
            "Available only for X11 sessions.",
        ),
        ScreenProvider(
            "hardware-kvm",
            "Relmote hardware KVM",
            False,
            True,
            True,
            "physical-device",
            "machine",
            "Available when a compatible Relmote video/input module is attached.",
        ),
    ]
    return tuple(providers)


def preferred_observe_provider() -> ScreenProvider | None:
    order = ("wayland-portal", "gnome-rdp", "vnc", "x11-native", "hardware-kvm")
    providers = {item.provider_id: item for item in discover_screen_providers()}
    for provider_id in order:
        item = providers[provider_id]
        if item.available and item.observe:
            return item
    return None
