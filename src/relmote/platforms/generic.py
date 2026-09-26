from __future__ import annotations

import os
import platform
import socket


class GenericPlatformAdapter:
    """Portable fallback used until a native adapter exists."""

    def observations(self) -> dict[str, dict]:
        return {
            "os": {
                "name": platform.system(),
                "release": platform.release(),
                "machine": platform.machine(),
                "evidence": "runtime-api",
            },
            "host": {
                "hostname": socket.gethostname(),
                "logical_cpu_count": os.cpu_count(),
                "evidence": "runtime-api",
            },
        }
