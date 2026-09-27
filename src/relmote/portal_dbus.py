from __future__ import annotations

import asyncio
import os
from dataclasses import dataclass
from uuid import uuid4

try:
    from dbus_next.aio import MessageBus
    from dbus_next import Message, MessageType, Variant
except ImportError:
    MessageBus = Message = MessageType = Variant = None


PORTAL = "org.freedesktop.portal.Desktop"
PORTAL_PATH = "/org/freedesktop/portal/desktop"
SCREENCAST = "org.freedesktop.portal.ScreenCast"
REQUEST = "org.freedesktop.portal.Request"


@dataclass(frozen=True)
class DbusPortalResponse:
    code: int
    results: dict


def _address() -> str:
    uid = os.getuid()
    runtime = os.environ.get("XDG_RUNTIME_DIR") or f"/run/user/{uid}"
    return (
        os.environ.get("DBUS_SESSION_BUS_ADDRESS")
        or f"unix:path={runtime}/bus"
    )


async def _connect():
    if MessageBus is None:
        raise RuntimeError("Linux screen support requires dbus-next")
    return await MessageBus(bus_address=_address()).connect()


async def _call(bus, member: str, signature: str, body: list):
    reply = await bus.call(
        Message(
            destination=PORTAL,
            path=PORTAL_PATH,
            interface=SCREENCAST,
            member=member,
            signature=signature,
            body=body,
        )
    )
    if reply.message_type == MessageType.ERROR:
        raise RuntimeError(
            f"{member} D-Bus error {reply.error_name}: "
            + (" ".join(map(str, reply.body)) if reply.body else "")
        )
    return reply


async def _request(
    bus,
    member: str,
    signature: str,
    body: list,
    *,
    timeout: float,
) -> DbusPortalResponse:
    loop = asyncio.get_running_loop()
    future = loop.create_future()
    request_path_holder = {"path": None}

    def handler(message):
        if (
            message.message_type == MessageType.SIGNAL
            and message.interface == REQUEST
            and message.member == "Response"
            and request_path_holder["path"] == message.path
            and not future.done()
        ):
            future.set_result(
                DbusPortalResponse(
                    code=int(message.body[0]),
                    results=dict(message.body[1]),
                )
            )
        return False

    bus.add_message_handler(handler)
    try:
        reply = await _call(bus, member, signature, body)
        if not reply.body:
            raise RuntimeError(f"{member} returned no request handle")
        request_path_holder["path"] = reply.body[0]
        return await asyncio.wait_for(future, timeout)
    finally:
        bus.remove_message_handler(handler)


async def _create_session(bus):
    token = "relmote_" + uuid4().hex
    response = await _request(
        bus,
        "CreateSession",
        "a{sv}",
        [{
            "handle_token": Variant("s", token + "_create"),
            "session_handle_token": Variant("s", token + "_session"),
        }],
        timeout=15,
    )
    if response.code != 0:
        raise PermissionError(f"CreateSession response {response.code}")
    value = response.results.get("session_handle")
    if value is None:
        raise RuntimeError("CreateSession returned no session_handle")
    return value.value


async def _select_sources(bus, session_handle: str):
    token = "relmote_" + uuid4().hex
    response = await _request(
        bus,
        "SelectSources",
        "oa{sv}",
        [
            session_handle,
            {
                "handle_token": Variant("s", token),
                "types": Variant("u", 1),
                "multiple": Variant("b", False),
                "cursor_mode": Variant("u", 2),
            },
        ],
        timeout=15,
    )
    if response.code != 0:
        raise PermissionError(f"SelectSources response {response.code}")


async def _start(bus, session_handle: str):
    token = "relmote_" + uuid4().hex
    response = await _request(
        bus,
        "Start",
        "osa{sv}",
        [
            session_handle,
            "",
            {"handle_token": Variant("s", token)},
        ],
        timeout=120,
    )
    if response.code != 0:
        raise PermissionError(f"Start response {response.code}")
    return response


async def _share():
    bus = await _connect()
    session = await _create_session(bus)
    await _select_sources(bus, session)
    return await _start(bus, session)


def request_monitor_share() -> DbusPortalResponse:
    return asyncio.run(_share())


async def _diagnose():
    lines = ["ScreenCast D-Bus diagnostic", "stage: CreateSession"]
    bus = await _connect()
    try:
        session = await _create_session(bus)
    except Exception as exc:
        lines.append(f"CreateSession FAILED: {type(exc).__name__}: {exc}")
        return lines
    lines.append(f"CreateSession OK: {session}")

    lines.append("stage: SelectSources")
    try:
        await _select_sources(bus, session)
    except Exception as exc:
        lines.append(f"SelectSources FAILED: {type(exc).__name__}: {exc}")
        return lines
    lines.append("SelectSources OK")

    lines.append("stage: Start")
    try:
        response = await _start(bus, session)
    except Exception as exc:
        lines.append(f"Start FAILED: {type(exc).__name__}: {exc}")
        return lines
    lines.append("Start OK")
    lines.append(repr(response.results))
    return lines


def diagnose() -> list[str]:
    return asyncio.run(_diagnose())
