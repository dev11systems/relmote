# Roadmap

Relmote should grow by validating one architectural layer at a time.

## Phase 0 — architecture

- [x] Define controller vs system transports.
- [x] Define policy as a mandatory execution boundary.
- [x] Define task semantics above transport.
- [x] Define initial capability vocabulary.
- [x] Define session and audit-log formats.
- [ ] Decide initial software/firmware/hardware licenses.

## Phase 1 — safe local prototype

Goal: prove that authorized structured intent can reach a target as USB HID input.

- [x] Dry-run transport.
- [x] Policy engine.
- [x] Structured action objects.
- [x] Exact-action approval in Assist mode.
- [x] Software session revoke/expiry behavior.
- [x] Replay protection for dispatched action IDs.
- [x] Metadata-only action audit log.
- [x] Linux USB HID text transport.
- [x] Pi USB gadget configuration scripts.
- [ ] Physical AUTHORIZE input.
- [ ] Physical STOP/revoke input.
- [ ] Visible armed/activity indicators.
- [ ] Validate HID output on sacrificial machine.
- [ ] Measure stop latency and verify no stuck keys.

Success criterion: an approved text action is emitted exactly once, and revoking authorization prevents further output.

## Phase 2 — bidirectional text

- [ ] USB CDC serial.
- [ ] Terminal helper/bridge design.
- [ ] Capture stdout/stderr where explicitly configured.
- [ ] Read-only diagnostic task loop.
- [ ] Transport-independent result objects.

## Phase 3 — companion control

- [ ] BLE control service.
- [ ] Phone/tablet companion UX.
- [ ] Bluetooth HID.
- [ ] Pairing and session display.
- [ ] Physical authorization/stop interaction.

## Phase 4 — direct IP path

- [ ] USB networking.
- [ ] Local Relmote API.
- [ ] Local web UI.
- [ ] SSH transport.
- [ ] Capability discovery and automatic path selection.

## Phase 5 — console and recovery

- [ ] TTL UART.
- [ ] RS-232 / console adapters.
- [ ] Optional Ethernet.
- [ ] KVM/video prototype.
- [ ] Boot/recovery workflows.

## Phase 6 — constrained and intermittent links

- [ ] Compact protocol encoding.
- [ ] Chunking and resumability.
- [ ] Store-and-forward.
- [ ] LoRa experiments.
- [ ] Meshtastic adapter.
- [ ] MeshCore adapter.
- [ ] Uniline/Unilink integration experiments.

## Phase 7 — out-of-band/native adapters

- [ ] Redfish.
- [ ] AMT where already configured.
- [ ] Additional platform management APIs.

## Hardware direction

Avoid custom PCB work until the transport, policy, and companion model have been validated on development hardware.


## Near-term software preview

- [x] Linux reference adapter
- [x] CLI/TUI/web frontends
- [x] shared in-process runtime
- [x] plain-language help
- [x] Full Check + deterministic network diagnosis
- [x] repo install/update workflow
- [x] remote-support availability policy
- [x] TUI/web support-policy controls
- [ ] local IPC/runtime socket
- [ ] persistent optional Agent service
- [ ] authenticated helper/controller identity
- [ ] Tailscale/private-network controller binding governed by support policy
- [ ] live frontend event updates
- [ ] interactive terminal session (SSH-backed first)
- [ ] browser terminal UI
- [ ] Linux screen observe backend (Wayland portal/PipeWire first where available)
- [ ] Linux screen control backend with separate input grant
- [ ] browser screen viewer/controller
- [ ] process/service/log diagnostics
- [ ] active connectivity tests
- [ ] workspace proposal approval UI
- [ ] external planner bridge MVP



## Future: self-hosted Relmote Hub / Console

Build an optional self-hosted control plane for people who administer or support multiple authorized Relmote nodes.

Potential scope:

- support a co-located Hub + Agent Host deployment as a first-class self-hosted topology;
- discover and organize software and hardware Relmote nodes;
- show node identity, availability, target, transport/path, and capability status;
- launch/revoke support sessions;
- aggregate diagnostics and attention items;
- open Terminal, Screen, Files/Workspace, and Agent sessions;
- surface permission requests and active grants;
- show audit/activity history;
- support groups/tags/locations without making physical location mandatory;
- coordinate software updates while preserving per-node authority;
- show exact version/build drift across Nodes and Agent Hosts before coordinating updates;
- provide presence/rendezvous for outbound-enrolled nodes without requiring per-target inbound setup;
- expose provider status such as Tailscale, LAN, SSH, RDP/VNC, portal/PipeWire, serial, and hardware KVM.

### Architectural constraint

The Hub is optional orchestration, not the root of trust.

A Relmote node must remain locally owned and useful without the Hub, a Dev11 service, cloud connectivity, or an Internet connection. Connecting a node to the Hub must not silently broaden controller authority or existing grants.

Hub and Agent Host may share a machine, but that must not make Hub process access equivalent to Agent Host credentials or target authority.

The first Hub MVP should be inventory/version/session coordination on top of already-validated Agent Host primitives, followed by outbound enrollment/rendezvous and only later optional relay.

This milestone follows the near-term single-node remote-support and Agent Bridge work.


## Near-term: Agent Host validation and MCP adapter

The repository-wide documentation reconciliation has landed. The next gate is real-machine validation of the independent Controller, Agent Host, and Target roles.

- [x] Define Controller, Agent Host, Target, and optional Hub roles.
- [x] Implement short-lived, single-use Agent pairing.
- [x] Store paired-target profiles locally with owner-only permissions.
- [x] Add Agent Host capability discovery.
- [x] Add paired-target status/list/read/allowlisted-exec operations.
- [x] Add a shared credential-blind paired-target service for CLI and future adapters.
- [x] Add a generalized multi-machine validation runbook.
- [ ] Complete Controller → Agent Host → Target real-machine validation.
- [ ] Verify consumed pairing-code rejection.
- [ ] Verify revocation invalidates the paired credential.
- [ ] Repeat with the Agent Host moved to another machine or platform where practical.
- [ ] Update current-status claims from observed validation evidence.
- [ ] Cut the next coherent development snapshot if warranted.
- [ ] Implement the first MCP/Codex adapter on top of the paired-target service.

The MCP adapter should not precede the baseline authority/revocation validation. It must not broaden target capabilities or expose profile bearer material.

