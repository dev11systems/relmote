from __future__ import annotations

import ipaddress
import shutil
import subprocess
from dataclasses import dataclass
from enum import Enum


class ExposureMode(str, Enum):
    LOCALHOST = "localhost"
    TAILSCALE = "tailscale"
    LAN = "lan"
    CUSTOM = "custom"


@dataclass(frozen=True)
class ExposureChoice:
    mode: ExposureMode
    bind_host: str
    description: str
    private: bool


def tailscale_ipv4() -> str | None:
    if shutil.which("tailscale") is None:
        return None
    try:
        completed = subprocess.run(
            ["tailscale", "ip", "-4"],
            capture_output=True,
            text=True,
            timeout=3,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if completed.returncode != 0:
        return None

    for raw in completed.stdout.splitlines():
        candidate = raw.strip()
        try:
            address = ipaddress.ip_address(candidate)
        except ValueError:
            continue
        if address.version == 4:
            return str(address)
    return None


def choose_exposure(mode: str = "auto", custom_host: str | None = None) -> ExposureChoice:
    if mode == "auto":
        ts = tailscale_ipv4()
        if ts:
            return ExposureChoice(
                ExposureMode.TAILSCALE,
                ts,
                "Private Tailscale interface",
                True,
            )
        return ExposureChoice(
            ExposureMode.LOCALHOST,
            "127.0.0.1",
            "This computer only",
            True,
        )

    if mode == "localhost":
        return ExposureChoice(
            ExposureMode.LOCALHOST,
            "127.0.0.1",
            "This computer only",
            True,
        )

    if mode == "tailscale":
        ts = tailscale_ipv4()
        if not ts:
            raise RuntimeError("Tailscale is not connected or has no IPv4 address")
        return ExposureChoice(
            ExposureMode.TAILSCALE,
            ts,
            "Private Tailscale interface",
            True,
        )

    if mode == "lan":
        return ExposureChoice(
            ExposureMode.LAN,
            "0.0.0.0",
            "All IPv4 interfaces (LAN/advanced)",
            False,
        )

    if mode == "custom":
        if not custom_host:
            raise ValueError("custom exposure requires a bind address")
        return ExposureChoice(
            ExposureMode.CUSTOM,
            custom_host,
            f"Custom interface: {custom_host}",
            False,
        )

    raise ValueError(f"unknown exposure mode: {mode}")
