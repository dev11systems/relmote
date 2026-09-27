# Relmote documentation map

This page is the navigation map for Relmote documentation. The root README is the project entry point; this map points to canonical deep dives.

## Start here

- `README.md` — what Relmote is, what works now, quick start, core roles, and project direction.
- `docs/STATUS.md` — canonical current implementation-status matrix.
- `docs/ROADMAP.md` — near-term and future work.
- `docs/ARCHITECTURE.md` — shared software/platform architecture.

## Authority, trust, and sessions

- `docs/TRUST.md` — trust and permission model.
- `docs/CAPABILITIES.md` — capability vocabulary and authorization.
- `docs/SESSIONS.md` — session lifecycle.
- `docs/IDENTITY.md` — node/target identity and ownership.
- `docs/SAFETY-INTERLOCK.md` — safety/stop concepts.
- `docs/DECISIONS.md` — durable architecture decisions.

## Remote support and user experience

- `docs/REMOTE-SUPPORT-UX.md` — remote-support interaction model.
- `docs/INTERACTIVE-SESSIONS.md` — interactive terminal/screen-style sessions.
- `docs/UX-PRINCIPLES.md` — UX principles.
- `docs/HELP-SYSTEM.md` — help/explanation model.
- `docs/DECISION-UX.md` — approval/decision interactions.
- `docs/TUI-DESIGN.md` — terminal UI direction.

## Agent access

- `docs/AGENT-BRIDGE.md` — target-side scoped Agent Bridge and authorization boundary.
- `docs/AGENT-HOST.md` — controller-side Agent Host role, pairing, and future MCP/Codex adapter.
- `docs/AGENT-HOST-VALIDATION.md` — reproducible Controller → Agent Host → Target validation runbook.
- `docs/USE-CASES-CODEX.md` — Codex-oriented use cases; treat implementation-status claims here as subordinate to `STATUS.md`.

## Screen and transports

- `docs/SCREEN-PROVIDERS.md` — pluggable screen observe/control providers.
- `docs/TRANSPORTS.md` — controller/system transport model.
- `software/TAILSCALE.md` — current direct-Tailscale binding model and optional Serve integration.
- `docs/PROTOCOL.md` — protocol direction.
- `docs/PLATFORM-SUPPORT.md` — platform support model.
- `docs/HID-TRANSPORT.md` — USB HID transport specifics.

## Software preview and operations

- `docs/INSTALL-FROM-REPO.md` — repository-preview installation.
- `docs/UPDATES.md` — update behavior.
- `docs/LINUX-PREVIEW.md` — Linux preview notes.
- `docs/RELEASE-PREVIEW.md` — preview release process.
- `docs/VERSIONING.md` — version/build identity.
- `docs/REPO-HYGIENE.md` — repository maintenance.
- `docs/PREVIEW-UX-CHECKLIST.md` — preview UX validation checklist.
- `docs/DEBUGGING.md` — local rotating debug logs and troubleshooting workflow.

## Hardware

- `docs/HARDWARE.md` — hardware strategy and relationship to software.
- `hardware/architecture/README.md` — hardware architecture.
- `hardware/concepts/README.md` — hardware form concepts.
- `hardware/modules/README.md` — modular hardware/reference modules.
- `hardware/industrial-design/README.md` — industrial-design work.
- `hardware/component-studies/README.md` — component studies.
- `docs/POWER.md` and `docs/COMPUTE.md` — hardware power/compute architecture.
- `docs/MODULARITY.md` — modularity model.

## Scenarios and planning

- `docs/USE-CASES.md` — use-case atlas.
- `docs/SCENARIOS.md` — scenarios.
- `docs/SCENARIO-MATRIX.md` — scenario/capability matrix.
- `docs/CAPABILITY-MAP.md` — capability placement/mapping.
- `docs/FEATURE-PLACEMENT.md` — where features belong in the architecture.

## Historical / validation-oriented material

Documents such as `docs/MVP.md`, `docs/FIRST-TEST.md`, `docs/SOFTWARE-PREVIEW-TEST.md`, and `docs/REMOTE-WORKSPACE-TEST.md` capture build/test sequences and may describe an earlier project state. They remain useful evidence and test guidance, but `README.md`, `STATUS.md`, and `ROADMAP.md` take precedence for current product/status claims.

## Documentation rule

When two documents disagree about whether a feature currently works, `docs/STATUS.md` is authoritative. Architecture/design documents may intentionally describe intended future behavior.

## Public documentation and privacy

Write public documentation for any operator, not around a maintainer's personal deployment. Describe roles such as Controller, Agent Host, and Target, with generic device classes and clearly fictional example names.

Do not copy personal machine names, usernames, home paths, private network addresses, tailnet domains, credentials, screenshots containing personal data, or other personal deployment details from conversations or test output into public docs, issues, or pull requests. Use placeholders such as `<agent-host>`, `<target>`, and `<workspace>` instead.

Real-world validation notes may describe relevant operating systems, device classes, versions, steps, and observed results after redaction. Product names may appear where compatibility or reproduction requires them, but must not imply that one person's hardware is required. Keep private deployment inventories and raw logs outside the public repository, and distinguish planned validation from completed tests.
