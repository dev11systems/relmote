from __future__ import annotations


CAPABILITY_LABELS = {
    "system.identify": "View computer identity",
    "system.platform": "View operating-system information",
    "system.memory": "View memory information",
    "system.uptime": "View uptime",
    "hardware.cpu": "View processor information",
    "storage.inspect": "View storage information",
    "network.inspect": "View network information",
    "network.dns": "View DNS settings",
    "logs.read": "View system logs",
    "file.read": "View files",
    "file.write": "Edit files",
    "input.keyboard": "Type on this computer",
    "observe.screen": "View this computer's screen",
}


def capability_label(capability: str) -> str:
    return CAPABILITY_LABELS.get(capability, capability.replace(".", " ").title())


def availability_label(value: str) -> str:
    return {
        "disabled": "Support off",
        "timed": "Support on temporarily",
        "until-disabled": "Support on until you turn it off",
    }.get(value, value)


def effect_label(value: str) -> str:
    return {
        "observation": "View information",
        "workspace-execution": "Run a project tool",
        "workspace-mutating": "Change project files/state",
        "system-mutating": "Change this computer",
    }.get(value, value)
