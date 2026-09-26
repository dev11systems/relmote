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
- [Roadmap](docs/ROADMAP.md)

## Current software proof

The repository now contains a transport-neutral execution boundary with:

- bounded target-specific grants;
- Observe / Teach / Assist / Operate modes;
- explicit capability checking;
- expiring and revocable sessions;
- exact-action approval in Assist mode;
- one-time action IDs to reject replay;
- privacy-conscious audit metadata;
- a no-side-effect dry-run transport.

Try the safe simulation after installing locally:

```bash
python -m pip install -e ".[test]"
relmote demo --mode assist --approve --text "hello from Relmote"
pytest -q
```

The dry-run transport reports what **would** have been dispatched but cannot emit real target input.

## Initial implementation path

1. Policy/session engine + dry-run transport. **← current**
2. USB HID proof-of-concept with explicit approval and immediate stop.
3. Bidirectional text feedback over USB serial.
4. BLE companion/control path and Bluetooth HID.
5. USB networking + local API/web UI.
6. SSH transport + capability-based path selection.
7. Physical serial console module.
8. KVM/video module.
9. Constrained mesh/store-and-forward operation.

## Status

**Early prototype.** Core authorization semantics are now executable; target-side hardware output is intentionally not implemented yet. The architecture is being validated before committing to custom hardware so that the project does not become accidentally shaped around one development board or one transport.

## Name

**Relmote** combines *relay*, *remote*, and *mote* (a small networked node).

## Safety and intended use

Relmote is intended for systems the operator owns or is authorized to administer. The project explicitly avoids stealth operation, silent privilege escalation, and hidden persistence.
