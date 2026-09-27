from __future__ import annotations

import json
import shutil
import subprocess


AGENT_PORT = 8788


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
    return {
        "available": True,
        "enabled": enabled,
        "url": None,
        "raw": value,
    }


def enable_private_transport() -> dict:
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


def disable_private_transport() -> dict:
    if not tailscale_available():
        return {"enabled": False, "kind": "none"}
    completed = subprocess.run(
        ["tailscale", "serve", "reset"],
        capture_output=True,
        text=True,
        timeout=15,
        check=False,
    )
    if completed.returncode != 0:
        raise RuntimeError(completed.stderr.strip() or "Could not reset Tailscale Serve")
    return {"enabled": False, "kind": "tailscale-serve"}
