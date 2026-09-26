# Relmote architecture

Relmote is a **portable intelligent interface node** between a controller and a target computing system.

The architecture deliberately separates **how the operator reaches Relmote** from **how Relmote reaches the target**.

```text
human / companion / agent
          │
   controller transport
          │
   ┌──────▼──────┐
   │   Relmote   │
   │             │
   │ identity    │
   │ session     │
   │ policy      │
   │ planner     │
   │ router      │
   │ audit log   │
   └──────┬──────┘
          │
     system transport
          │
  target computing system
```

## Major subsystems

### Identity

Tracks:

- the Relmote device itself;
- the controller;
- the target system;
- the current session;
- the cryptographic or physical proof used to authorize the session.

Target identity must be explicit when an operation could modify state.

### Capability discovery

Discovery answers questions such as:

- Can this target accept keyboard input?
- Is bidirectional serial available?
- Is there an authorized SSH endpoint?
- Is screen feedback available?
- Is an out-of-band interface present?
- What bandwidth, latency, reliability, and power constraints apply?

Discovery describes capability. It does **not** grant authority.

### Policy

The policy engine decides whether a proposed action is:

- allowed automatically;
- allowed only after approval;
- unavailable in the current mode;
- outside the current capability grant;
- forbidden.

Policy is deterministic and sits between model output and every state-changing transport.

### Planner

The planner turns intent into structured proposed actions. The planner may be local, phone-hosted, self-hosted, cloud-hosted, or absent entirely.

The planner never talks directly to target transports.

### Transport router

The router selects a suitable path from the currently available and authorized transports. It should prefer the richest, least-invasive useful path.

Example preference for a text-administration task:

```text
authorized native API / shell
        ↓ unavailable
bidirectional serial/network path
        ↓ unavailable
KVM with feedback
        ↓ unavailable
HID-only input
```

This is a preference, not a universal ordering. The task and permissions determine the appropriate route.

### Audit log

Every action proposal, approval, execution result, transport switch, privilege request, and session termination should be representable in the log.

## Separate planes

Relmote has three logically separate planes.

### Control plane

Carries:

- task intent;
- approvals;
- capability grants;
- session state;
- transport selection;
- status.

### Data plane

Carries the actual interaction:

- terminal text;
- commands;
- screen frames;
- keyboard/mouse events;
- files;
- API payloads.

### Safety plane

Remains authoritative even if the planner or data plane fails:

- physical stop;
- authorization timeout;
- target identity;
- mode switch;
- policy enforcement;
- session revocation.

## Modes

Relmote should support at least:

- **Observe** — receive information only.
- **Teach** — explain actions for the human to perform.
- **Assist** — prepare actions and require confirmation.
- **Operate** — execute within a bounded, explicit capability grant.

Mode is not the same as privilege. An Operate session can still be limited to read-only diagnostics.

## Graceful degradation

Relmote should preserve task meaning while changing transport.

A rich link might return complete logs. A constrained link might return a structured summary plus selected evidence. A disconnected controller may submit a store-and-forward task that runs later.

The task model therefore belongs above any individual transport.

## Hardware shape

The architecture should allow both:

- a single compact all-in-one unit;
- a small core plus optional modules such as console, KVM/video, Ethernet, or LoRa.

Custom hardware should follow the protocol and architecture, not define them.
