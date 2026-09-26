import json
from pathlib import Path

import pytest

from relmote.modules import ModuleDescriptor


ROOT = Path(__file__).resolve().parents[1]


def load_example(name: str) -> dict:
    return json.loads((ROOT / "examples" / "modules" / name).read_text())


def test_lora_module_descriptor_parses():
    descriptor = ModuleDescriptor.from_mapping(load_example("lora-mesh.json"))

    assert descriptor.module_id == "example.mesh.lora.v1"
    assert "radio.lora" in descriptor.capabilities
    assert descriptor.power.peak_mw == 1800
    assert descriptor.passthrough.power is True


def test_battery_can_source_power():
    descriptor = ModuleDescriptor.from_mapping(load_example("battery.json"))

    assert descriptor.power.can_source is True
    assert descriptor.power.source_peak_mw == 15000


def test_unknown_link_fails_closed():
    value = load_example("lora-mesh.json")
    value["links"].append("magic-bus")

    with pytest.raises(ValueError, match="unknown module links"):
        ModuleDescriptor.from_mapping(value)


def test_peak_power_cannot_be_below_typical():
    value = load_example("lora-mesh.json")
    value["power"]["peak_mw"] = 100

    with pytest.raises(ValueError, match="peak_mw"):
        ModuleDescriptor.from_mapping(value)


def test_module_capabilities_are_descriptive_not_authority():
    descriptor = ModuleDescriptor.from_mapping(load_example("lora-mesh.json"))

    # This is deliberately only a descriptive tuple. Authorization grants are
    # separate objects in relmote.model and cannot be created implicitly here.
    assert isinstance(descriptor.capabilities, tuple)
