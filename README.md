# Relmote

**A user-controlled interface layer for safely connecting people and agents to computing systems.**

Relmote is an experimental open platform for authorized remote support, diagnostics, agent access, and physical/digital computer interfaces. A Relmote node can be software running on a computer, dedicated hardware attached to one, or a hybrid of both.

The shared idea is simple: **connectivity is not authority**. Relmote keeps target identity, capabilities, approvals, active sessions, revocation, and evidence visible regardless of how a controller reaches a machine.

## What can Relmote do today?

The Linux-first software preview currently supports passive diagnostics, a CLI/TUI and private browser controller, explicit Remote Support availability, a normal-user browser terminal, and scoped Agent sessions for listing/reading approved workspaces and running allowlisted commands.

Agent Access is actively being developed around private transport, one-time pairing, and independent Agent Hosts. Wayland screen observation is also under active development: Relmote can discover relevant portal/provider capabilities, but browser screen streaming and graphical control are **not yet complete**.

See **[Current status](docs/STATUS.md)** for the canonical implemented / experimental / planned matrix.

## The four roles

Relmote separates roles that are often collapsed into one machine:

```text
       Controller
   (browser / iPad / CLI)
            │
            ▼
     optional Relmote Hub
            │
       Agent Host
 (Kaonashi, Falkor, server)
            │
            ▼
       Relmote Target
   (software or hardware node)
```

- **Controller** — the human-facing interface used to inspect, approve, revoke, and direct work.
- **Target / Node** — the computer or device being supported. It remains the authority boundary for its capabilities.
- **Agent Host** — optional compute that runs Codex or another agent elsewhere while using only the capabilities the target granted.
- **Hub** — a planned optional self-hosted multi-node console. It coordinates; it does not become the root of trust.

These roles can be on different devices. For example: an iPad can be the controller, an always-on home server the Agent Host, and a family member's computer the target.

## Software and hardware are one platform

Relmote is both software and hardware; neither is a secondary edition.

**Software Relmote** can run on an existing machine, VM, recovery environment, or other supported host. It can provide diagnostics, terminal/workspace access, agent sessions, and OS-native interaction paths.

**Hardware Relmote** carries the same identity/session/capability model outside the target OS. Hardware can eventually add USB HID, serial, KVM/video, pre-boot/recovery access, portable networking, physical authorization/STOP controls, and modular I/O.

Hybrid use is first-class: software and hardware nodes may cooperate.

## Authority model

Relmote is designed around a few durable rules:

- **Human authority first.** A reachable machine is not automatically an authorized machine.
- **Explicit capabilities.** Observe, terminal, workspace read/write, screen view/control, and other powers are separate grants.
- **Revocation matters.** Stopping support or revoking a session should invalidate its authority immediately.
- **Visible operation.** Active sessions, target identity, requested capabilities, and meaningful actions should be inspectable.
- **Least-invasive useful path.** Prefer a structured/native interface over emulating a keyboard when an authorized richer path exists.
- **No silent privilege escalation.** Administrative/elevated authority must be explicit.
- **Local/private operation where practical.** Cloud services are optional rather than fundamental to the architecture.

See [Trust and permissions](docs/TRUST.md), [Capabilities](docs/CAPABILITIES.md), and [Sessions](docs/SESSIONS.md).

## Try the Linux development preview

The easiest current repository install uses `pipx`:

```bash
pipx install 'relmote[screen-linux] @ git+https://github.com/dev11systems/relmote.git'
relmote
```

Update the preview:

```bash
relmote update
```

Check exactly what is installed:

```bash
relmote version
```

Relmote development snapshots use a human-readable revision such as `0.1.0-dev.11` plus an exact source build hash.

See [Install from repository](docs/INSTALL-FROM-REPO.md) and [Updates](docs/UPDATES.md) for details.

## Agent Access preview

Relmote's Agent Bridge is designed so an agent does **not** need to be installed on the target computer.

```text
iPad / browser
   Controller
       │
       ▼
Kaonashi / Falkor
   Agent Host
       │ scoped Relmote grant
       ▼
    Target PC
```

The target chooses an approved workspace and capabilities. Pairing uses a short-lived one-time code; the Agent Host receives only the authority contained in that target grant. Revocation remains target-controlled.

See [Agent Bridge](docs/AGENT-BRIDGE.md) and [Agent Host](docs/AGENT-HOST.md).

## Screen access

Screen access is modeled as a capability with interchangeable providers rather than one hard-coded implementation. Potential providers include Wayland portal/PipeWire, GNOME Remote Desktop/RDP, VNC, X11-native paths, VM consoles, and future hardware KVM.

`screen.observe` and `screen.control` are separate authorities. Observation should not silently alter the target's physical display topology.

See [Screen providers](docs/SCREEN-PROVIDERS.md).

## Hardware direction

Hardware concepts include Mini, Pocket, All-in-One, modular/DIY forms, USB HID/serial/networking, KVM/video, portable power, and physical safety controls. These are retained as a first-class track, but hardware maturity varies by component and should not be inferred from the software preview's status.

See [Hardware strategy](docs/HARDWARE.md) and [Hardware architecture](hardware/architecture/README.md).

## Project status

Relmote is an **active early prototype**. Some software paths are already useful for real-machine testing; Agent Host pairing, screen support, broader file/workspace operations, cross-platform adapters, the Hub, and physical hardware validation remain active work.

Do not infer availability from an architecture document alone. Use [Current status](docs/STATUS.md) for the current implementation snapshot.

## Documentation

Start with the **[documentation map](docs/README.md)** rather than an undifferentiated list of every design note.

Key documents:

- [Current status](docs/STATUS.md)
- [Roadmap](docs/ROADMAP.md)
- [Architecture](docs/ARCHITECTURE.md)
- [Platform model](docs/PLATFORM-MODEL.md)
- [Agent Bridge](docs/AGENT-BRIDGE.md)
- [Agent Host](docs/AGENT-HOST.md)
- [Remote-support UX](docs/REMOTE-SUPPORT-UX.md)
- [Screen providers](docs/SCREEN-PROVIDERS.md)
- [Hardware strategy](docs/HARDWARE.md)

## Name

**Relmote** combines *relay*, *remote*, and *mote* (a small networked node).

## Intended use

Relmote is intended for systems the operator owns or is authorized to administer. The project explicitly avoids stealth operation, hidden persistence, and silent privilege escalation.