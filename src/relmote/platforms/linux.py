from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path


def _read_os_release() -> dict[str, str]:
    result: dict[str, str] = {}
    path = Path("/etc/os-release")
    if not path.exists():
        return result
    try:
        for raw in path.read_text().splitlines():
            if "=" not in raw or raw.lstrip().startswith("#"):
                continue
            key, value = raw.split("=", 1)
            result[key] = value.strip().strip('"')
    except OSError:
        pass
    return result


def _run_json(argv: list[str]) -> object | None:
    try:
        completed = subprocess.run(
            argv,
            capture_output=True,
            text=True,
            timeout=5,
            check=False,
        )
    except (OSError, subprocess.TimeoutExpired):
        return None
    if completed.returncode != 0:
        return None
    try:
        return json.loads(completed.stdout)
    except json.JSONDecodeError:
        return None


class LinuxPlatformAdapter:
    """Linux-native passive/read-only observations."""

    def observations(self) -> dict[str, dict]:
        return {
            "linux.os": self.os_info(),
            "linux.network.interfaces": self.network_interfaces(),
            "linux.network.routes": self.network_routes(),
            "linux.services": self.services_summary(),
            "linux.block_devices": self.block_devices(),
        }

    def os_info(self) -> dict:
        value = _read_os_release()
        return {
            "pretty_name": value.get("PRETTY_NAME"),
            "id": value.get("ID"),
            "version_id": value.get("VERSION_ID"),
            "evidence": "/etc/os-release",
            "complete": bool(value),
        }

    def network_interfaces(self) -> dict:
        if not shutil.which("ip"):
            return {
                "interfaces": None,
                "evidence": "unavailable",
                "limitation": "iproute2 'ip' command not found",
            }
        value = _run_json(["ip", "-json", "address", "show"])
        return {
            "interfaces": value,
            "evidence": "ip -json address show" if value is not None else "unavailable",
            "complete": value is not None,
        }

    def network_routes(self) -> dict:
        if not shutil.which("ip"):
            return {
                "routes": None,
                "evidence": "unavailable",
                "limitation": "iproute2 'ip' command not found",
            }
        value = _run_json(["ip", "-json", "route", "show"])
        return {
            "routes": value,
            "evidence": "ip -json route show" if value is not None else "unavailable",
            "complete": value is not None,
        }

    def services_summary(self) -> dict:
        systemctl = shutil.which("systemctl")
        if not systemctl:
            return {
                "available": False,
                "evidence": "systemctl not found",
            }
        try:
            completed = subprocess.run(
                [
                    systemctl,
                    "--no-pager",
                    "--plain",
                    "--no-legend",
                    "--state=failed",
                    "--type=service",
                ],
                capture_output=True,
                text=True,
                timeout=5,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            return {"available": True, "failed_services": None, "evidence": "unavailable"}
        failed = [line for line in completed.stdout.splitlines() if line.strip()]
        return {
            "available": True,
            "failed_service_count": len(failed),
            "failed_services": failed[:50],
            "evidence": "systemctl --state=failed --type=service",
        }

    def block_devices(self) -> dict:
        if not shutil.which("lsblk"):
            return {
                "devices": None,
                "evidence": "unavailable",
                "limitation": "lsblk not found",
            }
        value = _run_json(
            ["lsblk", "--json", "--output", "NAME,TYPE,SIZE,FSTYPE,MOUNTPOINTS"]
        )
        return {
            "devices": value,
            "evidence": "lsblk --json",
            "complete": value is not None,
        }
