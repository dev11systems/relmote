from __future__ import annotations

import json
import os
from pathlib import Path


def profile_directory() -> Path:
    base = os.environ.get("XDG_CONFIG_HOME")
    if base:
        return Path(base) / "relmote" / "agents"
    return Path.home() / ".config" / "relmote" / "agents"


def _safe_name(name: str) -> str:
    value = "".join(
        ch if ch.isalnum() or ch in "-_." else "-"
        for ch in name.strip()
    ).strip(".-")
    return value or "relmote-target"


def save_profile(
    *,
    name: str,
    base_url: str,
    token: str,
    session: dict,
) -> Path:
    directory = profile_directory()
    directory.mkdir(parents=True, exist_ok=True, mode=0o700)

    path = directory / f"{_safe_name(name)}.json"
    value = {
        "name": name,
        "base_url": base_url.rstrip("/"),
        "token": token,
        "session": session,
    }
    encoded = json.dumps(value, indent=2).encode()

    fd = os.open(
        path,
        os.O_WRONLY | os.O_CREAT | os.O_TRUNC,
        0o600,
    )
    try:
        os.write(fd, encoded)
    finally:
        os.close(fd)
    os.chmod(path, 0o600)
    return path


def load_profile(name: str) -> dict:
    path = profile_directory() / f"{_safe_name(name)}.json"
    return json.loads(path.read_text())
