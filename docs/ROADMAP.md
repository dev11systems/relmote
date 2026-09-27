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

- discover and organize software and hardware Relmote nodes;
- show node identity, availability, target, transport/path, and capability status;
- launch/revoke support sessions;
- aggregate diagnostics and attention items;
- open Terminal, Screen, Files/Workspace, and Agent sessions;
- surface permission requests and active grants;
- show audit/activity history;
- support groups/tags/locations without making physical location mandatory;
- coordinate software updates while preserving per-node authority;
- expose provider status such as Tailscale, LAN, SSH, RDP/VNC, portal/PipeWire, serial, and hardware KVM.

### Architectural constraint

The Hub is optional orchestration, not the root of trust.

A Relmote node must remain locally owned and useful without the Hub, a Dev11 service, cloud connectivity, or an Internet connection. Connecting a node to the Hub must not silently broaden controller authority or existing grants.

This milestone follows the near-term single-node remote-support and Agent Bridge work.


## Near-term: documentation consolidation

After the first successful multi-machine Agent Host pairing test, perform a repository-wide documentation reconciliation.

Priorities:

1. Rewrite the root README as the current product/platform entry point.
2. Clearly distinguish current working preview features, experimental/in-progress features, and future concepts.
3. Explain the independent roles: Controller, Relmote Target/Node, Agent Host, and optional future Hub.
4. Present software and hardware as peer implementations of the shared Relmote authority/capability/session model.
5. Remove or relocate obsolete implementation-order/status claims from the README.
6. Reconcile overlapping architecture, capability, session, transport, remote-support, Agent Bridge, Agent Host, hardware, and roadmap documents.
7. Add a compact documentation map so readers can find canonical deep dives without a giant undifferentiated link list.
8. Mark historical design material as historical where it remains useful rather than silently mixing it with current behavior.
9. Verify install/update commands and current versioning behavior against the actual CLI.
10. Add a current-state matrix: implemented and tested; implemented but experimental; planned.

The README should answer, in order:

- What is Relmote?
- What can I do with it today?
- What are its roles/components?
- How do I install and try it?
- What security/authority guarantees matter?
- Where is it going?
- Where do I read deeper documentation?
