from __future__ import annotations

import platform
import shutil
import socket
import sys
from dataclasses import dataclass

from .agent import LocalAgent
from .version import build_info


@dataclass(frozen=True)
class DoctorCheck:
    name: str
    status: str
    message: str
    required: bool = False


def run_doctor_checks() -> tuple[DoctorCheck, ...]:
    checks: list[DoctorCheck] = []

    info = build_info()
    checks.append(
        DoctorCheck(
            "Relmote",
            "ok",
            f"{info['version']} · {info['channel']} · {info['commit']}",
            True,
        )
    )

    system = platform.system()
    checks.append(
        DoctorCheck(
            "Operating system",
            "ok" if system == "Linux" else "attention",
            f"{system} {platform.release()}",
            True,
        )
    )

    checks.append(
        DoctorCheck(
            "Python runtime",
            "ok" if sys.version_info >= (3, 11) else "attention",
            platform.python_version(),
            True,
        )
    )

    for command, label, required in (
        ("ip", "Network inspection (iproute2)", False),
        ("lsblk", "Storage inspection (lsblk)", False),
        ("systemctl", "systemd service inspection", False),
        ("ssh", "SSH target support", False),
        ("tailscale", "Tailscale integration", False),
    ):
        location = shutil.which(command)
        checks.append(
            DoctorCheck(
                label,
                "ok" if location else "optional-missing",
                location or f"{command} not found",
                required,
            )
        )

    try:
        agent = LocalAgent()
        snapshot = agent.snapshot()
        healthy = bool(snapshot.get("observations"))
        message = f"{len(snapshot.get('capabilities', []))} capabilities available"
    except Exception as exc:
        healthy = False
        message = f"{type(exc).__name__}: {exc}"

    checks.append(
        DoctorCheck(
            "Local diagnostics",
            "ok" if healthy else "failed",
            message,
            True,
        )
    )

    try:
        sock = socket.socket()
        sock.bind(("127.0.0.1", 0))
        port = sock.getsockname()[1]
        sock.close()
        web_ok = True
        web_message = f"localhost listener available (test port {port})"
    except OSError as exc:
        web_ok = False
        web_message = str(exc)

    checks.append(
        DoctorCheck(
            "Local web interface",
            "ok" if web_ok else "failed",
            web_message,
            True,
        )
    )

    return tuple(checks)


def doctor_exit_code(checks: tuple[DoctorCheck, ...]) -> int:
    return 1 if any(c.required and c.status == "failed" for c in checks) else 0


def print_doctor() -> int:
    checks = run_doctor_checks()
    print("RELMOTE DOCTOR\n")
    for check in checks:
        marker = {
            "ok": "✓",
            "attention": "!",
            "optional-missing": "○",
            "failed": "✗",
        }.get(check.status, "?")
        print(f"{marker} {check.name}")
        print(f"  {check.message}")
    print()
    missing = [c for c in checks if c.status == "optional-missing"]
    if missing:
        print("Optional features are unavailable until their tools are installed.")
    if doctor_exit_code(checks) == 0:
        print("Relmote's required preview checks passed.")
    else:
        print("One or more required preview checks failed.")
    return doctor_exit_code(checks)
