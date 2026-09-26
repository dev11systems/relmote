from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass


@dataclass(frozen=True)
class PortalEnvironment:
    uid: int
    runtime_dir: str
    bus_address: str
    portal_cli: str | None
    pipewire_cli: str | None

    @property
    def ready_for_portal_calls(self) -> bool:
        return bool(self.portal_cli and self.runtime_dir and self.bus_address)


def portal_environment() -> PortalEnvironment:
    uid = os.getuid()
    runtime_dir = os.environ.get("XDG_RUNTIME_DIR") or f"/run/user/{uid}"
    bus_address = (
        os.environ.get("DBUS_SESSION_BUS_ADDRESS")
        or f"unix:path={runtime_dir}/bus"
    )
    return PortalEnvironment(
        uid=uid,
        runtime_dir=runtime_dir,
        bus_address=bus_address,
        portal_cli=shutil.which("gdbus"),
        pipewire_cli=shutil.which("pw-cli"),
    )


def portal_screen_cast_available() -> tuple[bool, str]:
    env = portal_environment()
    if not env.ready_for_portal_calls:
        return False, "D-Bus portal tooling/session bus is unavailable."

    process_env = os.environ.copy()
    process_env["XDG_RUNTIME_DIR"] = env.runtime_dir
    process_env["DBUS_SESSION_BUS_ADDRESS"] = env.bus_address
    try:
        completed = subprocess.run(
            [
                env.portal_cli,
                "introspect",
                "--session",
                "--dest", "org.freedesktop.portal.Desktop",
                "--object-path", "/org/freedesktop/portal/desktop",
            ],
            capture_output=True,
            text=True,
            timeout=4,
            check=False,
            env=process_env,
        )
    except (OSError, subprocess.TimeoutExpired) as exc:
        return False, f"Portal introspection failed: {exc}"

    if completed.returncode != 0:
        return False, (
            completed.stderr.strip()
            or "Desktop portal did not respond on the graphical session bus."
        )

    if "org.freedesktop.portal.ScreenCast" not in completed.stdout:
        return False, "Desktop portal is present but ScreenCast is unavailable."

    return True, "Wayland ScreenCast portal is available."
