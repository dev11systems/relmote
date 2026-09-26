# Relmote Module Interface v0.1 — Draft

**Status:** architectural draft, not a frozen electrical standard.

This document defines the goals and logical layers of the optional Relmote snap-module ecosystem.

Exact pin counts, contact pitch, connector vendors, current limits, mechanical dimensions, and high-speed layout rules remain provisional until prototype validation.

## 1. Scope

The module interface exists to support compact integrated expansion while preserving ordinary standards such as USB-C for external hardware.

A Relmote implementation does **not** need this interface to be Relmote-compatible.

## 2. Physical layers

The reference interface has two logical physical layers.

### Layer A — service interface

Expected to carry:

- ground;
- module power;
- module presence;
- low-speed control;
- interrupt/wake;
- one or more low-speed serial links;
- optional USB 2.0.

This interface is intended for inexpensive modules.

### Layer B — optional high-speed interface

For modules requiring:

- video;
- high-speed storage;
- multi-gigabit networking;
- high-speed USB;
- PCIe-class connectivity;
- other signal-integrity-sensitive links.

Layer B is not required for ordinary modules.

## 3. Mechanical attachment

Reference snap modules should combine:

- magnetic alignment;
- keyed orientation;
- recessed contacts;
- a mechanical anti-shear feature.

Magnets alone must not be assumed to carry all mechanical loads.

Mechanical CAD will be part of the eventual normative specification.

## 4. Hot-plug philosophy

The module system should be designed as hot-plug-aware.

Insertion sequence should conceptually be:

```text
mechanical alignment
→ ground contact
→ presence detection
→ conservative power availability
→ descriptor discovery
→ negotiated power
→ data enable
→ capability publication
```

Removal should reverse this as safely as practical.

The final physical pin geometry should support the desired sequencing rather than relying entirely on software timing.

## 5. Module identity

Each module needs a stable identity mechanism that supports multiple simultaneously attached/stacked modules without address collision.

The final mechanism is intentionally not frozen in this draft.

Candidate approaches include:

- unique-ID device plus descriptor storage;
- small module-management MCU;
- dynamically addressable control bus;
- USB enumeration for modules already containing USB logic.

A fixed shared I²C EEPROM address is **not** sufficient for arbitrary stacked modules.

## 6. Module descriptor

A descriptor should minimally provide:

```yaml
module:
  vendor: example
  product: mesh-lora
  hardware_revision: 1
  serial: optional

protocol:
  descriptor_version: 1

power:
  typical_mw: 450
  peak_mw: 1800
  can_source: false

capabilities:
  - radio.lora
  - mesh.meshcore

links:
  - control
  - usb2

passthrough:
  power: true
  control: true
  usb2: false
  high_speed: false
```

The wire encoding may eventually use a compact binary format while retaining an equivalent human-readable representation.

## 7. Capability publication

Modules publish capabilities, not UI assumptions.

A LoRa module should say:

```text
radio.lora
```

rather than:

```text
show_the_lora_screen
```

This allows the same module to work with CLI, phone app, headless service, AI agent, or future interfaces.

## 8. Power negotiation

A module must not assume that physical attachment guarantees full operating power.

The host should determine:

- available power;
- startup budget;
- sustained budget;
- downstream pass-through budget.

A module may remain present but unavailable if power is insufficient.

## 9. Pass-through

Stackable modules explicitly declare what they pass downstream.

Possible resources:

- power;
- control;
- USB 2.0;
- high-speed lanes;
- wake/interrupt.

The topology must be discoverable.

## 10. Fault isolation

A faulty module should not be able to collapse the entire Relmote when reasonably preventable.

Reference designs should consider:

- per-module current limiting;
- switched power;
- ESD protection;
- reverse-current protection;
- fault reporting;
- software isolation;
- bus timeout/recovery.

## 11. Security

Physical attachment does not grant privileged software authority.

A module may add a capability, but use of that capability remains subject to normal Relmote session policy.

Untrusted third-party modules should be treated as hardware with potentially hostile firmware.

Future revisions may support signed module metadata, but signature verification must not become a proprietary vendor lock.

## 12. DIY requirements

The finished specification should be implementable using publicly available:

- connector/contact parts;
- magnets;
- PCB fabrication;
- open CAD;
- open firmware examples.

A hobbyist should be able to design a compatible module without reverse engineering a Dev11 product.

## 13. Standard external path

USB-C remains the recommended universal expansion path when:

- the module is external;
- high-speed signal integrity is easier through a standard cable/connector;
- the builder does not want to implement the snap interface;
- physical integration is unnecessary.

## 14. Open items before v1.0

- contact count;
- pogo/contact geometry;
- magnet geometry and polarity;
- mechanical latch/rail design;
- module voltage rails;
- maximum current;
- control-bus choice;
- unique identity mechanism;
- USB 2.0 routing rules;
- optional high-speed connector;
- hot-plug sequencing;
- stacking depth;
- thermal constraints;
- conformance test fixture.
