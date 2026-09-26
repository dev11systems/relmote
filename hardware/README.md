# Hardware

This directory tracks the **physical-device forms of the same Relmote platform** implemented by the software runtime.

Relmote hardware is not required for Relmote software to be useful. Its purpose is to extend the platform into situations software alone cannot cover well: pre-boot/firmware access, machines where nothing should be installed, USB HID, serial consoles, KVM/video, portable networking, physical safety interlocks, isolated target-facing I/O, and pocketable field support.

Hardware and software share the same conceptual contract:

- node and target identity;
- explicit session authority;
- capability discovery and grants;
- Observe / Teach / Assist / Operate semantics;
- visible activity and evidence;
- immediate STOP/revocation;
- transport independence;
- no silent privilege escalation.

## Planned stages

### `v0.1-pi-zero/`

Single-board bench proof:

```text
controller → Wi-Fi/BLE → Relmote → USB HID → test target
```

Goals:

- prove real HID output;
- prove exact-action approval;
- prove immediate revocation;
- prove visible activity;
- measure latency and reliability.

### `v0.2-safety-mcu/`

Split compute and safety planes.

Goals:

- MCU owns target-facing HID;
- authenticated internal command protocol;
- physical STOP enforced below the agent;
- watchdog/fail-closed behavior;
- later composite USB functions.

No custom PCB should be designed until these stages expose the actual requirements.


## Architecture and design

- [Hardware architecture](architecture/README.md)
- [Component studies](component-studies/README.md)
- [Industrial design](industrial-design/README.md)
- [Reference concepts](concepts/README.md)

The Pi Zero build is a prototype implementation, not the definition of Relmote hardware.


## Product forms

Current reference directions include:

- **Relmote Mini** — minimal embedded/interface node;
- **Relmote Pocket** — phone-sized portable field node;
- **Relmote All-in-One** — power-bank-sized integrated compute/network/I/O form;
- **Relmote modular stack** — magnetic/keyed optional modules with machine-readable descriptors;
- **DIY/custom Relmote** — open compatible implementations using standard USB-C or other supported links.

The physical product may be battery powered, USB-C powered, externally powered, or use combinations of these depending on form/module. USB-C remains a universal baseline even if optional pogo/contact modules are used.

## Relationship to the software-first preview

The Linux software preview is currently advancing faster because it lets the policy, permission, diagnostics, controller, terminal, screen, files, and planner semantics be tested on real machines before custom hardware exists.

Those validated semantics should flow downward into hardware. Hardware should add physical capabilities and stronger isolation—not fork into a separate Relmote protocol or UX.
