# Relmote

**A user-controlled interface layer for observing, supporting, and operating authorized computing systems.**

Relmote is an experimental open platform spanning software and hardware. It provides a common model for identity, capabilities, sessions, approvals, evidence, and transports so a person or authorized agent can work with a computer without treating connectivity as blanket permission.

Relmote can exist as software on the target, as separate hardware, or as a hybrid of both. The durable idea is the authority-aware interface layer—not one particular remote-desktop protocol, AI agent, transport, or enclosure.

## What works today

The active preview is Linux-first and software-first. Current exercised capabilities include:

- local diagnostics, observations, and support reports;
- CLI/TUI and a private browser controller;
- explicit Remote Support enable/disable state;
- normal-user browser terminal sessions with request/approval/revocation;
- scoped Agent sessions with list/read/allowlisted-exec capabilities;
- workspace confinement, scope warnings, revocation, and single-use pairing codes;
- repository install/update previews;
- Wayland/portal and screen-provider discovery foundations.

Screen streaming/control, cross-machine Agent Host workflows, Codex/MCP integration, richer file operations, the self-hosted Hub, cross-platform parity, and hardware validation are still in progress.

See **[Current status](docs/STATUS.md)** for the authoritative implemented / experimental / planned matrix.

## Core roles

Relmote separates roles that are often collapsed into one remote-access application:

```text
             Controller
          human-facing UI
     (browser / CLI / controller UI)
                 │
                 ▼
          optional Agent Host
       agent compute / adapters
     (workstation / server / appliance)
                 │
                 ▼
          Relmote Target / Node
       authority + capabilities
                 │
                 ▼
        authorized computing system
```

- **Controller** — where a person observes state, grants/revokes authority, and initiates work.
- **Agent Host** — optional compute host for Codex or another agent; it receives only capabilities granted by the target.
- **Target / Node** — the Relmote authority boundary associated with the system being supported.
- **Hub** — planned optional self-hosted orchestration for many nodes and Agent Hosts; not the root of trust.

These are roles, not fixed devices. One machine may fill several roles, and an Agent Host can move from one machine to another without silently changing target authority.

## Authority model

Relmote is designed around a few durable rules:

- **Connectivity does not imply permission.**
- **Human authority first.** Sensitive capabilities are explicit and revocable.
- **Observe and control are separate.** Viewing a screen must not automatically grant input control.
- **No silent privilege escalation.** Elevated actions require an appropriate grant.
- **Visible operation.** Active sessions, target identity, capabilities, and important actions should be inspectable.
- **Fail closed.** Ambiguous identity, lost authorization, or unknown actions should stop rather than guess.
- **Least-invasive useful path.** Prefer an authorized structured interface over pretending to be a keyboard or bypassing platform security.
- **Local-first where practical.** Cloud services and AI are optional components, not foundational authority.

## Software and hardware are peers

```text
                    RELMOTE
                       │
          ┌────────────┴────────────┐
          │                         │
     SOFTWARE NODE             HARDWARE NODE
 installed / temporary      Pocket / modular / KVM
 recovery / VM / target     HID / serial / pre-boot
          │                         │
          └────────────┬────────────┘
                       │
          shared identity / policy
          sessions / capabilities
             transports / evidence
```

A software node can provide diagnostics, terminal/workspace access, Agent Bridge capabilities, and eventually screen support without separate hardware.

Hardware extends the same model to cases software cannot cover well: firmware/boot access, USB HID, serial, isolated physical controls, video/KVM, portable networking, and systems where installing software is impossible or undesirable.

## Quick start: Linux development preview

Relmote is changing rapidly. `pipx` is the recommended repository-preview install path:

```bash
pipx install 'relmote[screen-linux] @ git+https://github.com/dev11systems/relmote.git'
relmote
```

Update the installed preview:

```bash
relmote update
relmote version
```

The browser URL printed by Relmote is the human controller. Remote/private exposure is explicit; Relmote should not silently publish a controller or Agent API to the public Internet.

See [Install from the repository](docs/INSTALL-FROM-REPO.md) and [Linux preview](docs/LINUX-PREVIEW.md) for details.

## Agent access

Relmote's Agent Bridge lets an agent running elsewhere work against a narrowly approved target scope without installing the agent runtime or its credentials on the target.

A representative deployment is:

```text
Browser / CLI          Agent Host                Relmote Target
   Controller   ───►  agent runtime / adapter ───► scoped authority
 approvals/revoke       Codex/MCP optional       local enforcement
```

Agent workspace list/read/execute permissions are separate grants. Pairing uses short-lived, single-use codes; revocation remains target-controlled. The current cross-machine Agent Host workflow is experimental.

See [Agent Bridge](docs/AGENT-BRIDGE.md) and [Agent Host](docs/AGENT-HOST.md).

## Screen support

Relmote treats screen access as a capability with interchangeable providers rather than hardcoding one remote-desktop implementation. Current Linux work includes Wayland portal/PipeWire, GNOME remote-desktop discovery, VNC/X11 possibilities, and future hardware KVM.

`screen.observe` and `screen.control` are intentionally separate. Screen observation should not silently alter physical display topology.

See [Screen providers](docs/SCREEN-PROVIDERS.md).

## Transports

Controller transports and target/system transports are independent. Depending on deployment, Relmote may use private IP networking, Tailscale, SSH, RDP/VNC, serial, USB networking, HID, BLE, KVM/video, or future constrained transports.

Transport availability does not create capability authority. See [Transport model](docs/TRANSPORTS.md).

## Project direction

Near-term work centers on:

1. hardening the Linux software preview and browser UX;
2. completing screen observation, then separately authorized graphical control;
3. proving multi-machine Agent Host pairing and adding a Codex/MCP adapter;
4. richer scoped file/workspace operations;
5. an optional self-hosted multi-node Relmote Hub;
6. continuing physical hardware validation using the same authority/session model.

See [Roadmap](docs/ROADMAP.md).

## Documentation

Start with:

- [Current status](docs/STATUS.md) — what is implemented, experimental, and planned.
- [Documentation map](docs/DOCS.md) — canonical deep dives and historical/validation docs.
- [Architecture](docs/ARCHITECTURE.md) — shared platform architecture.
- [Trust and permissions](docs/TRUST.md) — authority model.
- [Capabilities](docs/CAPABILITIES.md) — capability vocabulary.
- [Hardware strategy](docs/HARDWARE.md) — hardware/software relationship.
- [Roadmap](docs/ROADMAP.md) — where the project is going.

## Name

**Relmote** combines *relay*, *remote*, and *mote* (a small networked node).

## Safety and intended use

Relmote is intended only for systems the operator owns or is authorized to administer. The project explicitly rejects stealth operation, silent privilege escalation, and hidden persistence.

Relmote is an early prototype. Current behavior and interfaces can change between development snapshots.