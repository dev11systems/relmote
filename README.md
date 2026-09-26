# Relmote

**Portable, user-controlled intelligent interface node for connecting people and agents to computing systems across whatever authorized transports are available.**

Relmote is an experimental open platform for creating authorized, capability-aware interfaces between controllers and computing systems. A Relmote node may be physical hardware, installed or ephemeral software, a VM/container, a recovery environment, embedded firmware, or a hybrid of these. It is transport-agnostic by design: a controller might reach Relmote over BLE, Wi-Fi, Ethernet, the Internet, cellular, or a constrained mesh; Relmote might reach the target over USB HID, serial, SSH, USB networking, KVM, Redfish, or another adapter.

The durable abstraction is not “an AI keyboard” or even one physical gadget. It is an **authorized interface layer for computing systems**. Relmote Pocket is one portable hardware implementation.

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

- [Platform model](docs/PLATFORM-MODEL.md)
- [Architecture decisions](docs/DECISIONS.md)
- [UX principles](docs/UX-PRINCIPLES.md)
- [Preview UX checklist](docs/PREVIEW-UX-CHECKLIST.md)
- [MVP / build sequence](docs/MVP.md)
- [Linux Software Preview](docs/LINUX-PREVIEW.md)
- [CLI installation](docs/CLI-INSTALL.md)
- [Platform support](docs/PLATFORM-SUPPORT.md)
- [Identity & ownership](docs/IDENTITY.md)
- [Recovery](docs/RECOVERY.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Software architecture](software/README.md)
- [Transport model](docs/TRANSPORTS.md)
- [Capabilities](docs/CAPABILITIES.md)
- [Capability map](docs/CAPABILITY-MAP.md)
- [Feature placement](docs/FEATURE-PLACEMENT.md)
- [Scenario matrix](docs/SCENARIO-MATRIX.md)
- [Sessions](docs/SESSIONS.md)
- [Trust and permissions](docs/TRUST.md)
- [Protocol](docs/PROTOCOL.md)
- [Scenarios](docs/SCENARIOS.md)
- [Use-case atlas](docs/USE-CASES.md)
- [Hardware strategy](docs/HARDWARE.md)
- [Hardware architecture](hardware/architecture/README.md)
- [Modularity](docs/MODULARITY.md)
- [Power architecture](docs/POWER.md)
- [Compute architecture](docs/COMPUTE.md)
- [Hardware concepts](hardware/concepts/README.md)
- [Reference modules](hardware/modules/README.md)
- [Industrial design](hardware/industrial-design/README.md)
- [Component studies](hardware/component-studies/README.md)
- [Open specifications](spec/README.md)
- [USB HID transport](docs/HID-TRANSPORT.md)
- [Safety interlock](docs/SAFETY-INTERLOCK.md)
- [Roadmap](docs/ROADMAP.md)

## One platform, software and hardware

Relmote is both a **software system** and a **hardware platform**. Neither form is secondary.

A software-only Relmote can be installed on an existing computer, launched temporarily in a recovery environment, run in a VM/container, or exposed through an authorized private network. It can provide diagnostics, terminal access, files/workspaces, screen support, planners, and other capabilities without requiring a separate physical device.

A hardware Relmote carries the same authority/session/capability model outside the target computer. Hardware can add pre-boot access, USB HID, serial, KVM/video, isolated safety controls, portable networking, battery power, modular I/O, and access to systems where installing software is undesirable or impossible.

Hybrid use is first-class: software and hardware nodes can cooperate rather than compete.

```text
                     RELMOTE PLATFORM
                            │
              ┌─────────────┴─────────────┐
              │                           │
       RELMOTE SOFTWARE            RELMOTE HARDWARE
              │                           │
      installed / temporary       Pocket / All-in-One
      recovery / VM / agent       Mini / modular / DIY
              │                           │
              └─────────────┬─────────────┘
                            │
                shared identity / policy
               sessions / capabilities
                 transports / evidence
```

See [Software architecture](software/README.md) and [Hardware architecture](hardware/architecture/README.md).

## Platform forms

Relmote is intentionally not one fixed enclosure or deployment form.

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

## Try the Linux preview

During active development, the easiest repository install is with `pipx`:

```bash
pipx install 'git+https://github.com/dev11systems/relmote.git'
relmote
```

Upgrade the development preview:

```bash
relmote update
```

Or refresh it directly with pipx:

```bash
pipx install --force 'git+https://github.com/dev11systems/relmote.git'
```

Uninstall:

```bash
pipx uninstall relmote
```

See [Install from the repository](docs/INSTALL-FROM-REPO.md) for distro setup, pinning a commit/tag, and contributor options.

## Status

**Active early prototype — software-first validation, hardware track retained.**

The Linux software preview is now usable for real-machine testing and includes repository install/update, passive diagnostics, a TUI and private Tailscale web controller, explicit remote-support availability, a working normal-user browser PTY/terminal path, and graphical-session/Wayland discovery. Screen streaming, controller pairing, richer files/workspaces, planner bridges, and cross-platform adapters remain in development.

The hardware track remains first-class. Existing Pi Zero, HID, modularity, power, compute, enclosure, module, and safety-plane work is retained. Hardware validation should reuse the same session/capability/authorization semantics proven in software rather than becoming a separate product.

Near-term development therefore proceeds on two linked tracks:

1. **Software:** mature remote support (terminal → screen observe → files → pairing → controlled input), diagnostics, packaging, and Linux-first real-world testing.
2. **Hardware:** validate USB HID and physical AUTHORIZE/STOP, then add serial, USB networking, KVM/video, modular I/O, portable power, and integrated Pocket/All-in-One prototypes.

A capability should live in the shared core whenever possible; software/hardware-specific code belongs in adapters, transports, drivers, and physical modules.

## Name

**Relmote** combines *relay*, *remote*, and *mote* (a small networked node).

## Safety and intended use

Relmote is intended for systems the operator owns or is authorized to administer. The project explicitly avoids stealth operation, silent privilege escalation, and hidden persistence.
