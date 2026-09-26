# Relmote Pocket — reference concept

**Goal:** the everyday-carry Relmote.

Target character: **phone-sized footprint, thicker than a modern phone, genuinely pocketable, repairable, modular.**

## Reference envelope

The current v0.1 industrial-design target is:

```text
150 mm tall
72 mm wide
18 mm thick
```

This remains provisional pending physical prototyping.

See [Pocket envelope v0.1](../industrial-design/pocket-envelope-v0.1.md) for the dimensional layout.

The thickness budget is intentional. It creates room for:

- replaceable battery;
- robust USB-C connectors;
- screws;
- replaceable I/O daughterboard;
- thermal headroom;
- magnetic module structure.

## Conceptual layout

```text
╭────────────────────────────╮
│ RELMOTE                    │
│                            │
│      status display        │
│                            │
│ LINK   TARGET   ARMED      │
│                            │
│ [ AUTHORIZE ]      [ STOP ]│
├────────────────────────────┤
│ USB-C   USB-C   EXPANSION  │
╰────────────────────────────╯
             ║
       snap-module plane
```

## Baseline capabilities

A Pocket reference unit should aim to include:

- Linux-capable compute;
- independent safety MCU;
- Wi-Fi;
- BLE;
- USB target/device functionality;
- USB controller/expansion functionality;
- replaceable battery or removable battery subsystem;
- status UI;
- AUTHORIZE;
- STOP;
- open module interface.

## Internal architecture

```text
replaceable battery
        │
power-path board
        │
┌───────┴────────┐
│ compute        │
│                │
│ safety MCU     │
│                │
│ Wi-Fi / BLE    │
└───────┬────────┘
        │
replaceable I/O daughterboard
        │
USB-C / module interface
```

## Design priority

Pocket should remain useful without any module attached.

Modules should extend rather than complete the device.

## Likely users/scenarios

- everyday carry;
- helping family/friends with authorized devices;
- homelab maintenance;
- field diagnostics;
- portable AI/manual console;
- temporary KVM/serial/network access via modules.

## Avoid

- glued battery;
- mandatory cloud account;
- proprietary-only module interface;
- ultra-thin enclosure at the cost of repairability;
- permanently attached cellular/LoRa hardware when a module is sufficient.
