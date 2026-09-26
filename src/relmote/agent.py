from __future__ import annotations

import os
import platform
import shutil
import socket
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class AgentObservation:
    capability: str
    data: dict


class LocalAgent:
    """Narrow, read-only S1 Relmote Agent."""

    capabilities = frozenset(
        {
            "system.identify",
            "system.platform",
            "system.memory",
            "storage.inspect",
            "network.inspect",
        }
    )

    def observe(self, capability: str) -> AgentObservation:
        if capability not in self.capabilities:
            raise ValueError(f"unsupported S1 capability: {capability}")

        handlers = {
            "system.identify": self._identify,
            "system.platform": self._platform,
            "system.memory": self._memory,
            "storage.inspect": self._storage,
            "network.inspect": self._network,
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
        }

    def _platform(self) -> dict:
        return {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "python": platform.python_version(),
        }

    def _memory(self) -> dict:
        # Portable baseline without an external dependency.
        if hasattr(os, "sysconf"):
            try:
                pages = os.sysconf("SC_PHYS_PAGES")
                page_size = os.sysconf("SC_PAGE_SIZE")
                if isinstance(pages, int) and isinstance(page_size, int):
                    return {"physical_bytes": pages * page_size}
            except (ValueError, OSError):
                pass
        return {"physical_bytes": None}

    def _storage(self) -> dict:
        anchor = Path.home().anchor or "/"
        usage = shutil.disk_usage(anchor)
        return {
            "path": anchor,
            "total_bytes": usage.total,
            "used_bytes": usage.used,
            "free_bytes": usage.free,
        }

    def _network(self) -> dict:
        # S1 intentionally avoids shelling out to platform commands.
        addresses = []
        try:
            for item in socket.getaddrinfo(
                socket.gethostname(),
                None,
                type=socket.SOCK_STREAM,
            ):
                address = item[4][0]
                if address not in addresses:
                    addresses.append(address)
        except socket.gaierror:
            pass
        return {
            "hostname": socket.gethostname(),
            "addresses": addresses,
            "note": "portable S1 view; interface-level adapters come later",
        }
