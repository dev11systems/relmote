from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from uuid import uuid4

try:
    from dbus_next.aio import MessageBus
    from dbus_next import BusType, Variant
except ImportError:  # optional Linux screen extra
    MessageBus = None
    BusType = None
    Variant = None


PORTAL_NAME = "org.freedesktop.portal.Desktop"
PORTAL_PATH = "/org/freedesktop/portal/desktop"
SCREENCAST_IFACE = "org.freedesktop.portal.ScreenCast"
REQUEST_IFACE = "org.freedesktop.portal.Request"


@dataclass(frozen=True)
class DbusPortalResponse:
    code: int
    results: dict


def available() -> bool:
    return MessageBus is not None


async def _connect():
    if MessageBus is None:
        raise RuntimeError(
            "Linux screen support requires the screen-linux extra (dbus-next)"
        )
    uid = os.getuid()
    runtime = os.environ.get("XDG_RUNTIME_DIR") or f"/run/user/{uid}"
    address = (
        os.environ.get("DBUS_SESSION_BUS_ADDRESS")
        or f"unix:path={runtime}/bus"
    )
    return await MessageBus(bus_address=address).connect()


async def _portal_interface(bus):
    introspection = await bus.introspect(PORTAL_NAME, PORTAL_PATH)
    obj = bus.get_proxy_object(PORTAL_NAME, PORTAL_PATH, introspection)
    return obj.get_interface(SCREENCAST_IFACE)


async def _wait_request(bus, request_path: str, timeout: float):
    introspection = await bus.introspect(PORTAL_NAME, request_path)
    obj = bus.get_proxy_object(PORTAL_NAME, request_path, introspection)
    iface = obj.get_interface(REQUEST_IFACE)
    loop = asyncio.get_running_loop()
    future = loop.create_future()

    def response(code, results):
        if not future.done():
            future.set_result(DbusPortalResponse(int(code), dict(results)))

    iface.on_response(response)
    try:
        return await asyncio.wait_for(future, timeout=timeout)
    finally:
        try:
            iface.off_response(response)
        except Exception:
            pass


async def _create_session():
    bus = await _connect()
    iface = await _portal_interface(bus)
    token = "relmote_" + uuid4().hex
    options = {
        "handle_token": Variant("s", token + "_create"),
        "session_handle_token": Variant("s", token + "_session"),
    }
    request_path = await iface.call_create_session(options)
    response = await _wait_request(bus, request_path, 15)
    if response.code != 0:
        raise PermissionError(f"CreateSession response {response.code}")
    handle = response.results.get("session_handle")
    if handle is None:
        raise RuntimeError("CreateSession returned no session_handle")
    return bus, iface, handle.value


async def _request_monitor_share():
    bus, iface, session_handle = await _create_session()

    select_token = "relmote_" + uuid4().hex
    select_path = await iface.call_select_sources(
        session_handle,
        {
            "handle_token": Variant("s", select_token),
            "types": Variant("u", 1),
            "multiple": Variant("b", False),
            "cursor_mode": Variant("u", 2),
        },
    )
    selected = await _wait_request(bus, select_path, 15)
    if selected.code != 0:
        raise PermissionError(f"SelectSources response {selected.code}")

    start_token = "relmote_" + uuid4().hex
    start_path = await iface.call_start(
        session_handle,
        "",
        {"handle_token": Variant("s", start_token)},
    )
    started = await _wait_request(bus, start_path, 120)
    if started.code != 0:
        raise PermissionError(f"Start response {started.code}")
    return started


def request_monitor_share() -> DbusPortalResponse:
    return asyncio.run(_request_monitor_share())


async def _diagnose():
    lines = ["ScreenCast D-Bus diagnostic", "stage: CreateSession"]
    try:
        bus, iface, session_handle = await _create_session()
    except Exception as exc:
        lines.append(f"CreateSession FAILED: {type(exc).__name__}: {exc}")
        return lines
    lines.append(f"CreateSession OK: {session_handle}")

    lines.append("stage: SelectSources")
    token = "relmote_" + uuid4().hex
    try:
        path = await iface.call_select_sources(
            session_handle,
            {
                "handle_token": Variant("s", token),
                "types": Variant("u", 1),
                "multiple": Variant("b", False),
                "cursor_mode": Variant("u", 2),
            },
        )
        response = await _wait_request(bus, path, 15)
        if response.code != 0:
            raise PermissionError(f"response {response.code}")
    except Exception as exc:
        lines.append(f"SelectSources FAILED: {type(exc).__name__}: {exc}")
        return lines
    lines.append("SelectSources OK")

    lines.append("stage: Start")
    token = "relmote_" + uuid4().hex
    try:
        path = await iface.call_start(
            session_handle,
            "",
            {"handle_token": Variant("s", token)},
        )
        response = await _wait_request(bus, path, 120)
        if response.code != 0:
            raise PermissionError(f"response {response.code}")
    except Exception as exc:
        lines.append(f"Start FAILED: {type(exc).__name__}: {exc}")
        return lines
    lines.append("Start OK")
    lines.append(repr(response.results))
    return lines


def diagnose() -> list[str]:
    return asyncio.run(_diagnose())
