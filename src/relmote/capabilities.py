from __future__ import annotations

from enum import Enum


class Capability(str, Enum):
    """Initial Relmote capability vocabulary.

    Capability names are wire-level identifiers. Additions should be deliberate
    because grants may persist across transports and software versions.
    """

    SYSTEM_IDENTIFY = "system.identify"

    OBSERVE_CONSOLE = "observe.console"
    OBSERVE_SCREEN = "observe.screen"

    INPUT_KEYBOARD = "input.keyboard"
    INPUT_POINTER = "input.pointer"

    SHELL_READ = "shell.read"
    SHELL_WRITE = "shell.write"

    FILE_READ = "file.read"
    FILE_WRITE = "file.write"

    NETWORK_INSPECT = "network.inspect"
    NETWORK_CONFIGURE = "network.configure"

    POWER_READ = "power.read"
    POWER_CONTROL = "power.control"

    STORAGE_READ = "storage.read"
    STORAGE_WRITE = "storage.write"

    FIRMWARE_READ = "firmware.read"
    FIRMWARE_WRITE = "firmware.write"

    PRIVILEGE_ELEVATE = "privilege.elevate"


KNOWN_CAPABILITIES = frozenset(cap.value for cap in Capability)
