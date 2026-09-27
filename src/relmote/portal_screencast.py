from __future__ import annotations

import os
import re
import shutil
import subprocess
import time
import selectors
from dataclasses import dataclass
from uuid import uuid4


@dataclass(frozen=True)
class PortalResponse:
    code: int
    results_text: str


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


def _request_path(token: str) -> str:
    # The portal returns this path from the method call, but listening to the
    # desktop portal before the call avoids losing a fast Response signal.
    return token


def _portal_request(
    method: str,
    method_args: tuple[str, ...],
    options: dict[str, str],
    *,
    timeout_seconds: int = 30,
) -> PortalResponse:
    token = "relmote_" + uuid4().hex
    options = dict(options)
    options["handle_token"] = "<'%s'>" % token

    monitor = subprocess.Popen(
        [
            _gdbus(),
            "monitor",
            "--session",
            "--dest", "org.freedesktop.portal.Desktop",
        ],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        env=_portal_env(),
    )
    try:
        time.sleep(0.08)
        options_text = "{" + ", ".join(
            "'%s': %s" % (key, value) for key, value in options.items()
        ) + "}"
        completed = subprocess.run(
            [
                _gdbus(),
                "call",
                "--session",
                "--dest", "org.freedesktop.portal.Desktop",
                "--object-path", "/org/freedesktop/portal/desktop",
                "--method", f"org.freedesktop.portal.ScreenCast.{method}",
                *method_args,
                options_text,
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

        deadline = time.monotonic() + timeout_seconds
        captured: list[str] = []
        assert monitor.stdout is not None
        selector = selectors.DefaultSelector()
        selector.register(monitor.stdout, selectors.EVENT_READ)
        while time.monotonic() < deadline:
            remaining = max(0.0, deadline - time.monotonic())
            events = selector.select(timeout=min(0.25, remaining))
            if not events:
                continue
            line = monitor.stdout.readline()
            if not line:
                continue
            captured.append(line.strip())
            joined = " ".join(captured[-20:])
            if "Response" not in joined:
                continue
            code_match = re.search(r"uint32\s+(\d+)", joined)
            if code_match:
                return PortalResponse(
                    code=int(code_match.group(1)),
                    results_text=joined,
                )
        raise RuntimeError(
            f"{method}: portal response was not received before {timeout_seconds}s"
        )
    finally:
        monitor.terminate()
        try:
            monitor.wait(timeout=1)
        except subprocess.TimeoutExpired:
            monitor.kill()


def create_session() -> str:
    token = "relmote_session_" + uuid4().hex
    response = _portal_request(
        "CreateSession",
        (),
        {"session_handle_token": "<'%s'>" % token},
    )
    if response.code != 0:
        raise PermissionError(
            f"ScreenCast session was declined or cancelled (response {response.code})"
        )
    match = re.search(
        r"session_handle[^']*'(/org/freedesktop/portal/desktop/session/[^']+)'",
        response.results_text,
    )
    if not match:
        raise RuntimeError(
            "ScreenCast CreateSession succeeded but no session handle was returned"
        )
    return match.group(1)


def select_monitor(session_handle: str) -> None:
    response = _portal_request(
        "SelectSources",
        (session_handle,),
        {
            "types": "<uint32 1>",
            "multiple": "<false>",
            "cursor_mode": "<uint32 2>",
        },
    )
    if response.code != 0:
        raise PermissionError(
            f"screen source selection was declined or cancelled (response {response.code})"
        )


def start_screen_cast(session_handle: str) -> PortalResponse:
    response = _portal_request(
        "Start",
        (session_handle, "''"),
        {},
        timeout_seconds=120,
    )
    if response.code != 0:
        raise PermissionError(
            f"screen sharing was declined or cancelled (response {response.code})"
        )
    return response


def request_monitor_share() -> PortalResponse:
    session_handle = create_session()
    select_monitor(session_handle)
    return start_screen_cast(session_handle)


def diagnose_portal_flow() -> list[str]:
    lines = ["ScreenCast portal diagnostic"]
    lines.append("stage: CreateSession")
    try:
        session_handle = create_session()
    except Exception as exc:
        lines.append(f"CreateSession FAILED: {type(exc).__name__}: {exc}")
        return lines
    lines.append(f"CreateSession OK: {session_handle}")

    lines.append("stage: SelectSources")
    try:
        select_monitor(session_handle)
    except Exception as exc:
        lines.append(f"SelectSources FAILED: {type(exc).__name__}: {exc}")
        return lines
    lines.append("SelectSources OK")

    lines.append("stage: Start")
    try:
        response = start_screen_cast(session_handle)
    except Exception as exc:
        lines.append(f"Start FAILED: {type(exc).__name__}: {exc}")
        return lines
    lines.append("Start OK")
    lines.append(response.results_text)
    return lines
