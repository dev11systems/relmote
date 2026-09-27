from __future__ import annotations

import json
import logging
import shutil
import subprocess


AGENT_PORT = 8788
LOGGER = logging.getLogger("relmote.agent_access")


def tailscale_available() -> bool:
    return shutil.which("tailscale") is not None


def serve_status() -> dict:
    if not tailscale_available():
        return {"available": False, "enabled": False, "url": None}
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
            "url": None,
            "detail": completed.stderr.strip(),
        }
    try:
        value = json.loads(completed.stdout or "{}")
    except json.JSONDecodeError:
        value = {}
    text = completed.stdout
    enabled = f"127.0.0.1:{AGENT_PORT}" in text or f"localhost:{AGENT_PORT}" in text

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
        "url": urls[0] if urls else None,
        "raw": value,
    }


def enable_private_transport() -> dict:
    if not tailscale_available():
        LOGGER.error("Cannot enable Agent Access: Tailscale is not installed")
        raise RuntimeError("Tailscale is not installed")

    LOGGER.info("Enabling private Agent Access with Tailscale Serve on port %s", AGENT_PORT)
    try:
        completed = subprocess.run(
            ["tailscale", "serve", "--bg", str(AGENT_PORT)],
            capture_output=True,
            text=True,
            timeout=30,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        LOGGER.exception(
            "Tailscale Serve timed out while enabling Agent Access on port %s",
            AGENT_PORT,
        )
        raise RuntimeError(
            "Tailscale Serve did not return within 30 seconds. "
            "Check tailscale serve status and relmote logs."
        ) from exc

    if completed.returncode != 0:
        detail = completed.stderr.strip() or "Tailscale Serve failed"
        LOGGER.error(
            "Tailscale Serve failed while enabling Agent Access: returncode=%s stderr=%s",
            completed.returncode,
            detail,
        )
        raise RuntimeError(detail)

    LOGGER.info("Private Agent Access transport enabled")
    return {
        "enabled": True,
        "kind": "tailscale-serve",
        "detail": completed.stdout.strip(),
    }


def disable_private_transport() -> dict:
    if not tailscale_available():
        return {"enabled": False, "kind": "none"}

    LOGGER.info("Disabling private Agent Access transport on port %s", AGENT_PORT)
    try:
        completed = subprocess.run(
            ["tailscale", "serve", str(AGENT_PORT), "off"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except subprocess.TimeoutExpired as exc:
        LOGGER.exception(
            "Tailscale Serve timed out while disabling Agent Access on port %s",
            AGENT_PORT,
        )
        raise RuntimeError(
            "Tailscale Serve did not return while disabling Agent Access. "
            "Check tailscale serve status and relmote logs."
        ) from exc

    if completed.returncode != 0:
        detail = completed.stderr.strip() or "Could not disable Relmote Agent Serve mapping"
        LOGGER.error(
            "Tailscale Serve failed while disabling Agent Access: returncode=%s stderr=%s",
            completed.returncode,
            detail,
        )
        raise RuntimeError(detail)

    LOGGER.info("Private Agent Access transport disabled")
    return {"enabled": False, "kind": "tailscale-serve"}
