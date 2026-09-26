from __future__ import annotations

import os
import platform
import shutil
import socket
import time
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AgentObservation:
    capability: str
    data: dict


class LocalAgent:
    """Narrow, read-only software Relmote Agent.

    S2 favors Python/OS APIs and passive inspection. Active connectivity probes
    are intentionally not part of the default Observe capability set.
    """

    capabilities = frozenset(
        {
            "system.identify",
            "system.platform",
            "system.memory",
            "system.uptime",
            "hardware.cpu",
            "storage.inspect",
            "network.inspect",
            "network.dns",
        }
    )

    def observe(self, capability: str) -> AgentObservation:
        if capability not in self.capabilities:
            raise ValueError(f"unsupported S2 capability: {capability}")

        handlers = {
            "system.identify": self._identify,
            "system.platform": self._platform,
            "system.memory": self._memory,
            "system.uptime": self._uptime,
            "hardware.cpu": self._cpu,
            "storage.inspect": self._storage,
            "network.inspect": self._network,
            "network.dns": self._dns,
        }
        return AgentObservation(capability, handlers[capability]())

    def snapshot(self) -> dict:
        return {
            "capabilities": sorted(self.capabilities),
            "observations": {
                cap: self.observe(cap).data for cap in sorted(self.capabilities)
            },
        }

    def _identify(self) -> dict:
        return {
            "hostname": socket.gethostname(),
            "fqdn": socket.getfqdn(),
            "evidence": "local-os-api",
        }

    def _platform(self) -> dict:
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "python": platform.python_version(),
            "evidence": "local-runtime-api",
        }

    def _memory(self) -> dict:
        physical = None
        if hasattr(os, "sysconf"):
            try:
                pages = os.sysconf("SC_PHYS_PAGES")
                page_size = os.sysconf("SC_PAGE_SIZE")
                if isinstance(pages, int) and isinstance(page_size, int):
                    physical = pages * page_size
            except (ValueError, OSError):
                pass
        return {
            "physical_bytes": physical,
            "evidence": "local-os-api",
            "complete": physical is not None,
        }

    def _uptime(self) -> dict:
        # Linux provides a stable kernel API. Other OS adapters come later.
        uptime = None
        proc = Path("/proc/uptime")
        if proc.exists():
            try:
                uptime = float(proc.read_text().split()[0])
            except (OSError, ValueError, IndexError):
                pass
        return {
            "seconds": uptime,
            "evidence": "local-os-api" if uptime is not None else "unavailable",
            "complete": uptime is not None,
        }

    def _cpu(self) -> dict:
        return {
            "logical_count": os.cpu_count(),
            "machine": platform.machine(),
            "processor": platform.processor() or None,
            "evidence": "local-runtime-api",
        }

    def _storage(self) -> dict:
        anchor = Path.home().anchor or "/"
        usage = shutil.disk_usage(anchor)
        return {
            "path": anchor,
            "total_bytes": usage.total,
            "used_bytes": usage.used,
            "free_bytes": usage.free,
            "percent_used": round((usage.used / usage.total) * 100, 1)
            if usage.total else None,
            "evidence": "local-os-api",
        }

    def _network(self) -> dict:
        addresses = []
        try:
            for item in socket.getaddrinfo(
                socket.gethostname(), None, type=socket.SOCK_STREAM
            ):
                address = item[4][0]
                if address not in addresses:
                    addresses.append(address)
        except socket.gaierror:
            pass

        classifications = []
        for address in addresses:
            if address.startswith("127.") or address == "::1":
                kind = "loopback"
            elif address.startswith("169.254.") or address.lower().startswith("fe80:"):
                kind = "link-local"
            else:
                kind = "configured"
            classifications.append({"address": address, "kind": kind})

        return {
            "hostname": socket.gethostname(),
            "addresses": classifications,
            "evidence": "local-name-resolution-api",
            "limitations": [
                "S2 does not yet enumerate every interface/route portably",
                "no external connectivity probe was performed",
            ],
        }

    def _dns(self) -> dict:
        servers = []
        search = []
        resolv = Path("/etc/resolv.conf")
        if resolv.exists():
            try:
                for raw in resolv.read_text().splitlines():
                    line = raw.strip()
                    if not line or line.startswith("#"):
                        continue
                    parts = line.split()
                    if len(parts) >= 2 and parts[0] == "nameserver":
                        servers.append(parts[1])
                    elif len(parts) >= 2 and parts[0] in {"search", "domain"}:
                        search.extend(parts[1:])
            except OSError:
                pass
        return {
            "servers": servers,
            "search": search,
            "evidence": "resolver-config" if resolv.exists() else "unavailable",
            "limitations": [
                "resolver configuration is not proof that DNS resolution works"
            ],
        }
