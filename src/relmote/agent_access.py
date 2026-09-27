from __future__ import annotations

import json
import logging
import shutil
import subprocess

from .agent_server import start_tailscale_agent_api
from .network_exposure import tailscale_ipv4


AGENT_PORT = 8788
LOGGER = logging.getLogger("relmote.agent_access")


def tailscale_available() -> bool:
    return shutil.which("tailscale") is not None


def direct_transport_status(runtime) -> dict:
    address = tailscale_ipv4()
    listener = getattr(runtime, "_agent_direct_listener", None)
    running = bool(listener is not None and listener.running)
    bound_address = getattr(listener, "host", None) if running else None

    detail = None
    if running and address and bound_address != address:
        detail = (
            "Agent API is bound to a previous Tailscale address; "
            "disable and re-enable Agent Access."
        )

    return {
        "available": bool(address),
        "enabled": running,
        "kind": "tailscale-direct",
        "address": address,
        "bound_address": bound_address,
        "url": (
            f"http://{bound_address}:{AGENT_PORT}"
            if running and bound_address
            else None
        ),
        "detail": detail,
    }


def enable_direct_transport(runtime) -> dict:
    address = tailscale_ipv4()
    if not address:
        LOGGER.error(
            "Cannot enable direct Agent Access: Tailscale has no IPv4 address"
        )
        raise RuntimeError("Tailscale is not connected or has no IPv4 address")

    current = getattr(runtime, "_agent_direct_listener", None)
    if current is not None and current.running:
        if current.host == address:
            return direct_transport_status(runtime)
        current.stop()

    LOGGER.info(
        "Binding Agent API directly to Tailscale address %s:%s",
        address,
        AGENT_PORT,
    )
    try:
        listener = start_tailscale_agent_api(runtime, AGENT_PORT)
    except OSError as exc:
        LOGGER.exception(
            "Could not bind Agent API to Tailscale address %s:%s",
            address,
            AGENT_PORT,
        )
        raise RuntimeError(
            f"Could not bind Agent API to Tailscale address {address}:{AGENT_PORT}: "
            f"{exc}"
        ) from exc

    setattr(runtime, "_agent_direct_listener", listener)
    LOGGER.info("Direct Tailscale Agent Access enabled at %s:%s", address, AGENT_PORT)
    return direct_transport_status(runtime)


def disable_direct_transport(runtime) -> dict:
    listener = getattr(runtime, "_agent_direct_listener", None)
    if listener is not None:
        LOGGER.info(
            "Stopping direct Tailscale Agent API listener at %s:%s",
            listener.host,
            listener.port,
        )
        listener.stop()
        setattr(runtime, "_agent_direct_listener", None)
    return direct_transport_status(runtime)


# Tailscale Serve remains an optional convenience path. It is no longer the
# default Agent Access transport because Serve may require tailnet-admin setup
# that a shared-in target or ordinary operator cannot perform.
def tailscale_serve_status() -> dict:
    if not tailscale_available():
        return {
            "available": False,
            "enabled": False,
            "kind": "tailscale-serve",
            "url": None,
        }
    completed = subprocess.run(
        ["tailscale", "serve", "status", "--json"],
        capture_output=True,
        text=True,
        timeout=8,
        check=False,
    )
    if completed.returncode != 0:
        return {
            "available": True,
            "enabled": False,
            "kind": "tailscale-serve",
            "url": None,
            "detail": completed.stderr.strip(),
        }
    try:
        value = json.loads(completed.stdout or "{}")
    except json.JSONDecodeError:
        value = {}
    text = completed.stdout
    enabled = (
        f"127.0.0.1:{AGENT_PORT}" in text
        or f"localhost:{AGENT_PORT}" in text
    )

    urls: list[str] = []

    def collect_urls(item):
        if isinstance(item, dict):
            for key, child in item.items():
                if isinstance(key, str) and key.startswith("https://"):
                    urls.append(key.rstrip("/"))
                collect_urls(child)
        elif isinstance(item, list):
            for child in item:
                collect_urls(child)
        elif isinstance(item, str) and item.startswith("https://"):
            urls.append(item.rstrip("/"))

    collect_urls(value)

    return {
        "available": True,
        "enabled": enabled,
        "kind": "tailscale-serve",
        "url": urls[0] if urls else None,
        "raw": value,
    }


def enable_tailscale_serve() -> dict:
    if not tailscale_available():
        raise RuntimeError("Tailscale is not installed")
    completed = subprocess.run(
        ["tailscale", "serve", "--bg", str(AGENT_PORT)],
        capture_output=True,
        text=True,
        timeout=30,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "Tailscale Serve failed")
    return {
        "enabled": True,
        "kind": "tailscale-serve",
        "detail": completed.stdout.strip(),
    }


def disable_tailscale_serve() -> dict:
    if not tailscale_available():
        return {"enabled": False, "kind": "tailscale-serve"}
    completed = subprocess.run(
        ["tailscale", "serve", str(AGENT_PORT), "off"],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(
            completed.stderr.strip()
            or "Could not disable Relmote Agent Serve mapping"
        )
    return {"enabled": False, "kind": "tailscale-serve"}


serve_status = tailscale_serve_status
enable_private_transport = enable_tailscale_serve
disable_private_transport = disable_tailscale_serve
