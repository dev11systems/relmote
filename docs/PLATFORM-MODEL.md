# Relmote platform model

Relmote is **not inherently a physical device**.

Relmote is an open platform for creating authorized, capability-aware interfaces between controllers and computing systems across whatever transports are available.

## Core abstractions

```text
                         RELMOTE PLATFORM

 Controller implementations                    Node implementations
 ──────────────────────────                    ────────────────────
 iOS / iPadOS                                 software agent
 Android / GrapheneOS                         Pocket hardware
 Web / PWA                                    Mini hardware
 CLI / TUI                                    All-in-One hardware
 desktop                                      VM / container
 third-party                                  live/recovery environment
                                              embedded firmware
                 \                              /
                  \                            /
                   └──── Relmote protocols ───┘
                              │
                       target systems
```

## Node

A **Relmote node** participates in Relmote identity, capability, task, policy, evidence, and transport semantics.

A node may be physical hardware, installed software, ephemeral software, a VM, a container, a bootable recovery environment, embedded firmware, a gateway, or a hybrid composition.

## Controller

A **Relmote controller** is how a human or authorized upstream system interacts with nodes: phone, tablet, browser, CLI, TUI, desktop application, or another Relmote.

## Target

A target is the computing system being observed or operated. A node and target may inhabit the same physical computer.

```text
laptop
├─ target OS
└─ relmoted software node
```



## Agent Host

An **Agent Host** is optional compute that runs an agent or agent adapter away from the target while using only capabilities granted by the target Relmote node.

Controller and Agent Host are separate roles. An iPad/browser may supervise a session while Kaonashi, Falkor, or another server performs agent compute.

The Agent Host cannot manufacture target authority; it consumes scoped grants issued by the target/controller model.

## Hub

A future **Relmote Hub** is an optional self-hosted multi-node controller/orchestration layer.

The Hub may organize targets, Agent Hosts, sessions, diagnostics, and permission requests, but it is not the root of trust. Nodes remain independently usable and enforce their own grants.

## Planner

A planner is optional: human, deterministic automation, local AI, phone AI, self-hosted AI, or cloud AI.

Relmote remains useful without one.

## Physical Relmote

Physical implementations earn their existence when software alone cannot provide the required capability:

- pre-OS interaction;
- broken-OS recovery;
- KVM/video;
- USB HID;
- serial;
- physical STOP;
- independent networking;
- radio/mesh;
- no-install temporary support;
- isolated safety plane.

## Software Relmote

Software implementations are preferable when the target OS is healthy and native integration is available.

They may expose richer capabilities such as shell, filesystem, logs, processes, package management, network state, and structured OS APIs.

## Hybrid

Hardware and software may cooperate.

```text
controller
    │
    ▼
Relmote Pocket
    │
    ├── KVM/HID ──────┐
    │                  │
    └── USB network ─► Relmote Agent
                       │
                       ▼
                     target
```

The controller sees available paths/capabilities and Relmote selects the least-invasive useful authorized path. If the software agent disappears, the hardware path may remain.

## Principle

> **Do not require hardware when software is sufficient; do not require target software when hardware can provide the needed interface.**

This is a central Relmote design rule.
