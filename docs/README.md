# Relmote documentation

This directory contains Relmote's deeper design and implementation documentation. Start with the root README and current status, then follow the canonical topic pages below.

## Start here

- `../README.md` — project entry point and quick start.
- `STATUS.md` — canonical current implementation-status matrix.
- `ROADMAP.md` — near- and long-term direction.
- `ARCHITECTURE.md` — shared platform architecture.

## Authority, identity, sessions, and safety

- `TRUST.md` — trust and permission model.
- `IDENTITY.md` — node/target identity and ownership.
- `SESSIONS.md` — session model.
- `CAPABILITIES.md` — capability semantics.
- `SAFETY-INTERLOCK.md` — safety/interlock principles.
- `DECISIONS.md` — durable architecture decisions.

## Remote support and interaction

- `REMOTE-SUPPORT-UX.md` — remote-support interaction model.
- `INTERACTIVE-SESSIONS.md` — interactive terminal/session architecture.
- `SCREEN-PROVIDERS.md` — pluggable screen observation/control providers.
- `HELP-SYSTEM.md` — built-in help architecture.

## Agents and multi-machine operation

- `AGENT-BRIDGE.md` — target-side scoped Agent Bridge.
- `AGENT-HOST.md` — controller-side Agent Host role and adapter boundary.
- `USE-CASES-CODEX.md` — Codex-oriented use cases.
- `REMOTE-WORKSPACE-TEST.md` — remote workspace validation material.

## Platform and transports

- `PLATFORM-MODEL.md` — forms/roles across software and hardware.
- `TRANSPORTS.md` — controller and target transport model.
- `PROTOCOL.md` — protocol concepts.
- `PLATFORM-SUPPORT.md` — platform support strategy.
- `MODULARITY.md` — modular platform design.

## Hardware

- `HARDWARE.md` — hardware strategy.
- `HID-TRANSPORT.md` — USB HID transport.
- `POWER.md` — power architecture.
- `COMPUTE.md` — compute architecture.
- `../hardware/architecture/README.md` — hardware architecture.

## Development and preview operations

- `INSTALL-FROM-REPO.md` — development-preview installation.
- `UPDATES.md` — update behavior.
- `VERSIONING.md` — version/build identity.
- `LINUX-PREVIEW.md` — Linux preview details.
- `RELEASE-PREVIEW.md` — preview/release process.
- `REPO-HYGIENE.md` — repository maintenance conventions.

## Design/supporting material

Documents such as scenario matrices, use-case atlases, decision UX, feature placement, TUI design, preview checklists, and test guides provide supporting detail. They should not override the canonical current status or architecture documents above.

Where an older document describes an implementation sequence or status that conflicts with `STATUS.md`, treat `STATUS.md` as current.