from __future__ import annotations

import platform

from .base import PlatformAdapter
from .generic import GenericPlatformAdapter
from .linux import LinuxPlatformAdapter


def current_platform_adapter() -> PlatformAdapter:
    if platform.system() == "Linux":
        return LinuxPlatformAdapter()
    return GenericPlatformAdapter()
