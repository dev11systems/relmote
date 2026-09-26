# Relmote

**Portable, user-controlled intelligent interface node for connecting people and agents to computing systems across whatever authorized transports are available.**

Relmote is an experimental Dev11 project exploring a small physical node that can sit between a human or AI controller and a target computing system. It is transport-agnostic by design: a controller might reach Relmote over BLE, Wi-Fi, Ethernet, the Internet, cellular, or a constrained mesh; Relmote might reach the target over USB HID, serial, SSH, USB networking, KVM, Redfish, or another adapter.

The durable abstraction is not “an AI keyboard.” It is an **authorized interface router for computing systems**.

## Core model

```text
controller / agent
        │
 controller transport
        │
   ┌────▼─────┐
   │ Relmote  │
   │ identity │
   │ policy   │
   │ routing  │
   │ logging  │
   └────┬─────┘
        │
  system transport
        │
 target computing system
```

Controller transports and system transports are independent. A phone can control Relmote over BLE while Relmote types over USB HID; a remote user can reach it over a constrained mesh while Relmote talks to a router over serial; a local tablet can supervise a session while Relmote uses SSH.

## Principles

- **Human authority first.** Connectivity does not imply permission.
- **Visible operation.** No stealth mode; actions, target identity, permissions, and active sessions should be inspectable.
- **Graceful degradation.** Prefer rich structured interfaces, but fall back to simpler paths when necessary.
- **Transport independence.** Tasks and approvals should survive changes in bearer or interface.
- **Least-invasive useful path.** If an authorized SSH session exists, do not pretend to be a keyboard.
- **Fail closed.** Unknown actions, lost authorization, or ambiguous target identity stop execution.
- **Local-first where practical.** Cloud AI is optional, not a hardware requirement.
- **No silent privilege escalation.** Elevated actions require explicit capability grants.

## Transport families

**Controller transports** connect a person, companion app, or agent to Relmote: BLE, Wi-Fi, Ethernet, Internet/cellular, USB, LoRa/mesh, and future Uniline/Unilink integration.

**System transports** connect Relmote to the target: USB/Bluetooth HID, USB CDC serial, physical serial, USB networking, SSH, KVM, Redfish/AMT, and future adapters.

See:

- [Architecture](docs/ARCHITECTURE.md)
- [Transport model](docs/TRANSPORTS.md)
- [Capabilities](docs/CAPABILITIES.md)
- [Sessions](docs/SESSIONS.md)
- [Trust and permissions](docs/TRUST.md)
- [Protocol](docs/PROTOCOL.md)
- [Scenarios](docs/SCENARIOS.md)
- [Hardware strategy](docs/HARDWARE.md)
- [Modularity](docs/MODULARITY.md)
- [Power architecture](docs/POWER.md)
- [Compute architecture](docs/COMPUTE.md)
- [Hardware concepts](hardware/concepts/README.md)
- [Industrial design](hardware/industrial-design/README.md)
- [Open specifications](spec/README.md)
- [USB HID transport](docs/HID-TRANSPORT.md)
- [Safety interlock](docs/SAFETY-INTERLOCK.md)
- [Roadmap](docs/ROADMAP.md)

## Platform forms

Relmote is intentionally not one fixed enclosure.

Reference forms currently include:

- **Mini** — minimal MCU-class node;
- **Pocket** — phone-sized everyday-carry reference design;
- **All-in-One** — power-bank-sized integrated field design;
- **DIY/custom** — any compatible implementation that follows the protocol and authorization model.

The optional snap-module system is designed around an open magnetic/keyed attachment with a service/contact layer for ordinary modules and a separate optional high-speed layer for demanding modules. USB-C remains a first-class universal expansion path; the snap ecosystem is never mandatory.

Module descriptors are machine-readable and publish hardware/resource capabilities, power requirements, links, and pass-through behavior. Module capabilities do **not** become authorization grants automatically.

## Current prototype

The repository now contains:

- bounded target-specific grants;
- Observe / Teach / Assist / Operate modes;
- explicit capability checking;
- expiring and revocable sessions;
- exact-action approval in Assist mode;
- one-time action IDs to reject replay;
- privacy-conscious audit metadata;
- a no-side-effect dry-run transport;
- a narrow Linux USB HID text transport with no raw-report interface;
- Raspberry Pi Zero-class USB gadget setup/teardown scripts.

Try the safe simulation after installing locally:

```bash
python -m pip install -e ".[test]"
relmote demo --mode assist --approve --text "hello from Relmote"
pytest -q
```

The real HID transport exists in software but has **not yet been validated on physical target hardware**.

## Initial implementation path

1. Policy/session engine + dry-run transport. **complete**
2. USB HID software transport + Pi gadget configuration. **implemented; physical validation next**
3. Physical AUTHORIZE/STOP controls and sacrificial-target test.
4. Bidirectional text feedback over USB serial.
5. BLE companion/control path and Bluetooth HID.
6. USB networking + local API/web UI.
7. SSH transport + capability-based path selection.
8. Physical serial console module.
9. KVM/video module.
10. Constrained mesh/store-and-forward operation.

## Status

**Early prototype.** The software authorization boundary and first target transport are executable and covered by CI. The next milestone is hardware validation on a sacrificial machine with physical authorization and STOP controls.

## Name

**Relmote** combines *relay*, *remote*, and *mote* (a small networked node).

## Safety and intended use

Relmote is intended for systems the operator owns or is authorized to administer. The project explicitly avoids stealth operation, silent privilege escalation, and hidden persistence.
