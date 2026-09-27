# Relmote current status

This document is the canonical high-level implementation-status snapshot. Detailed design documents describe intended architecture; this page distinguishes what is working from what remains experimental or planned.

## Implemented and exercised

- Linux software-node identity, passive diagnostics, and support reports.
- Local TUI/CLI and private browser controller.
- Explicit Remote Support enable/disable policy.
- Normal-user browser terminal sessions with explicit request/approval/revocation.
- Repository install and self-update preview flow.
- Wayland graphical-session and xdg-desktop-portal discovery.
- Scoped Agent sessions with list/read/allowlisted-exec capabilities.
- Agent workspace confinement, including traversal and symlink-escape protection.
- Agent session revocation and bearer rejection after revocation.
- Short-lived, single-use Agent pairing codes.
- Direct private Agent Access bound to the target's exact Tailscale interface, including transport shutdown/re-enable behavior.
- Cross-machine Agent Host pairing and paired-target status/list/read/allowlisted-exec operations.
- Target-side Agent revocation invalidating already-paired Agent Host credentials.
- Agent Host capability discovery.
- Target-home workspace defaults, scope warnings, and home-confined path suggestions.

## Implemented, actively experimental

- Cross-platform/private-transport portability beyond the exercised Linux direct-Tailscale path.
- Wayland ScreenCast portal integration.
- Screen-provider discovery/selection architecture.
- Browser Agent Access UI and modular JavaScript migration.
- Local stdio MCP/Codex Agent Host adapter exposing paired-target status/list/read and constrained exec operations; real Codex validation is pending.

These paths are under active real-machine validation and may change between development snapshots.

## Planned / not yet complete

- Actual screen pixels rendered in the Relmote browser viewer.
- Graphical keyboard/pointer control.
- General file/workspace editing through the browser.
- Production credential/keyring storage for Agent Hosts.
- Self-hosted multi-node Relmote Hub/Console, including co-located Hub + Agent Host deployment.
- Cross-platform target adapters beyond the Linux-first preview.
- Physical hardware validation of the current hardware concepts and transports.
- Hardware KVM/video and mature physical control modules.

## Status vocabulary

- **Implemented and exercised**: code exists and the relevant path has been exercised in development/testing.
- **Experimental**: code exists but integration, UX, portability, or real-machine behavior is still being validated.
- **Planned**: design intent exists but the capability should not be presented as available.

Status is capability-specific. A broad subsystem may contain items in more than one category.

## Current reference roles

A useful current deployment model is:

- **Controller:** a browser, CLI, or other human-facing interface on a phone, tablet, or computer.
- **Agent Host:** a laptop, workstation, server, or VM providing agent compute and adapters.
- **Target / Node:** the authorized computer or system being observed, diagnosed, or controlled.
- **Hub:** a future optional self-hosted multi-node orchestration layer.

These are roles, not fixed products. One machine may fill multiple roles, and changing Agent Host does not itself change target authority.

## Security note

Connectivity does not imply authority. Remote Support, terminal sessions, Agent grants, workspace capabilities, pairing, and future screen control are separate boundaries.

Relmote remains an early prototype, not a security-certified product. Use it only with systems the operator owns or is authorized to administer.
