from __future__ import annotations

import os
import re
import shutil
import subprocess
from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class PortalRequest:
    token: str
    request_path: str


def _portal_env() -> dict[str, str]:
    env = os.environ.copy()
    uid = os.getuid()
    runtime = env.get("XDG_RUNTIME_DIR") or f"/run/user/{uid}"
    env["XDG_RUNTIME_DIR"] = runtime
    env["DBUS_SESSION_BUS_ADDRESS"] = (
        env.get("DBUS_SESSION_BUS_ADDRESS")
        or f"unix:path={runtime}/bus"
    )
    return env


def _gdbus() -> str:
    command = shutil.which("gdbus")
    if not command:
        raise RuntimeError("gdbus is required for the Wayland ScreenCast preview")
    return command


def _call(method: str, *args: str) -> str:
    completed = subprocess.run(
        [
            _gdbus(),
            "call",
            "--session",
            "--dest", "org.freedesktop.portal.Desktop",
            "--object-path", "/org/freedesktop/portal/desktop",
            "--method", f"org.freedesktop.portal.ScreenCast.{method}",
            *args,
        ],
        capture_output=True,
        text=True,
        timeout=8,
        check=False,
        env=_portal_env(),
    )
    if completed.returncode != 0:
        raise RuntimeError(
            completed.stderr.strip() or f"ScreenCast {method} failed"
        )
    return completed.stdout.strip()


def create_session_request() -> PortalRequest:
    token = "relmote_" + uuid4().hex
    output = _call(
        "CreateSession",
        "{'handle_token': <'%s'>, 'session_handle_token': <'%s_session'>}"
        % (token, token),
    )
    match = re.search(r"'(/org/freedesktop/portal/desktop/request/[^']+)'", output)
    if not match:
        raise RuntimeError(f"could not parse portal request path: {output}")
    return PortalRequest(token=token, request_path=match.group(1))
