from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping


_ALLOWED_LINKS = frozenset(
    {
        "control",
        "uart",
        "i2c",
        "spi",
        "gpio",
        "usb2",
        "high_speed",
    }
)


@dataclass(frozen=True)
class ModulePower:
    typical_mw: int
    peak_mw: int
    can_source: bool
    source_peak_mw: int | None = None


@dataclass(frozen=True)
class ModulePassthrough:
    power: bool
    control: bool
    usb2: bool
    high_speed: bool


@dataclass(frozen=True)
class ModuleDescriptor:
    """Transport-neutral description of an attached Relmote module.

    Module capabilities describe hardware/resources that become available.
    They are NOT authorization grants and must never be copied directly into a
    user/session permission set.
    """

    module_id: str
    vendor: str
    product: str
    hardware_revision: str
    firmware_revision: str | None
    serial: str | None
    descriptor_version: int
    capabilities: tuple[str, ...]
    links: tuple[str, ...]
    power: ModulePower
    passthrough: ModulePassthrough

    @classmethod
    def from_mapping(cls, value: Mapping[str, Any]) -> "ModuleDescriptor":
        module = _mapping(value, "module")
        protocol = _mapping(value, "protocol")
        power = _mapping(value, "power")
        passthrough = _mapping(value, "passthrough")

        descriptor_version = _int(protocol, "descriptor_version")
        if descriptor_version != 1:
            raise ValueError(
                f"unsupported module descriptor version: {descriptor_version}"
            )

        capabilities = _string_sequence(value, "capabilities")
        links = _string_sequence(value, "links")

        unknown_links = sorted(set(links) - _ALLOWED_LINKS)
        if unknown_links:
            raise ValueError(f"unknown module links: {', '.join(unknown_links)}")

        typical_mw = _nonnegative_int(power, "typical_mw")
        peak_mw = _nonnegative_int(power, "peak_mw")
        if peak_mw < typical_mw:
            raise ValueError("power.peak_mw must be >= power.typical_mw")

        can_source = _bool(power, "can_source")
        source_peak = power.get("source_peak_mw")
        if source_peak is not None:
            if isinstance(source_peak, bool) or not isinstance(source_peak, int):
                raise ValueError("power.source_peak_mw must be an integer")
            if source_peak < 0:
                raise ValueError("power.source_peak_mw must be non-negative")
        if not can_source and source_peak not in (None, 0):
            raise ValueError(
                "power.source_peak_mw requires power.can_source=true"
            )

        module_id = _string(module, "id")
        if not _identifier(module_id):
            raise ValueError(f"invalid module id: {module_id!r}")

        for capability in capabilities:
            if not _identifier(capability):
                raise ValueError(f"invalid module capability: {capability!r}")

        return cls(
            module_id=module_id,
            vendor=_string(module, "vendor"),
            product=_string(module, "product"),
            hardware_revision=str(module.get("hardware_revision")),
            firmware_revision=_optional_stringish(module.get("firmware_revision")),
            serial=_optional_stringish(module.get("serial")),
            descriptor_version=descriptor_version,
            capabilities=tuple(capabilities),
            links=tuple(links),
            power=ModulePower(
                typical_mw=typical_mw,
                peak_mw=peak_mw,
                can_source=can_source,
                source_peak_mw=source_peak,
            ),
            passthrough=ModulePassthrough(
                power=_bool(passthrough, "power"),
                control=_bool(passthrough, "control"),
                usb2=_bool(passthrough, "usb2"),
                high_speed=_bool(passthrough, "high_speed"),
            ),
        )


def _mapping(value: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    item = value.get(key)
    if not isinstance(item, Mapping):
        raise ValueError(f"{key} must be an object")
    return item


def _string(value: Mapping[str, Any], key: str) -> str:
    item = value.get(key)
    if not isinstance(item, str) or not item:
        raise ValueError(f"{key} must be a non-empty string")
    return item


def _int(value: Mapping[str, Any], key: str) -> int:
    item = value.get(key)
    if isinstance(item, bool) or not isinstance(item, int):
        raise ValueError(f"{key} must be an integer")
    return item


def _nonnegative_int(value: Mapping[str, Any], key: str) -> int:
    item = _int(value, key)
    if item < 0:
        raise ValueError(f"{key} must be non-negative")
    return item


def _bool(value: Mapping[str, Any], key: str) -> bool:
    item = value.get(key)
    if not isinstance(item, bool):
        raise ValueError(f"{key} must be a boolean")
    return item


def _string_sequence(value: Mapping[str, Any], key: str) -> list[str]:
    item = value.get(key)
    if not isinstance(item, list) or any(not isinstance(x, str) for x in item):
        raise ValueError(f"{key} must be an array of strings")
    if len(set(item)) != len(item):
        raise ValueError(f"{key} must not contain duplicates")
    return item


def _optional_stringish(value: Any) -> str | None:
    if value is None:
        return None
    if isinstance(value, bool):
        raise ValueError("revision/serial values cannot be booleans")
    if isinstance(value, (str, int)):
        return str(value)
    raise ValueError("revision/serial values must be string, integer, or null")


def _identifier(value: str) -> bool:
    if not value:
        return False
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789._-")
    return value[0].isalnum() and value == value.lower() and all(
        ch in allowed for ch in value
    )
