# Relmote MVP and build sequence

> **Historical build-sequence note:** this document records the software-first milestone sequence that helped bootstrap the current preview. It is no longer the canonical current-status tracker. See [STATUS.md](STATUS.md) and [ROADMAP.md](ROADMAP.md) for current state and priorities.

Relmote's **first deployable implementation is software-first**.

The hardware track remains important, but Pocket should prove why physical Relmote is useful rather than be required before anyone can use the platform.

## Software MVP success criteria

A user can:

1. download/install or temporarily run Relmote on a computer;
2. open a local browser controller;
3. see node and target identity/capabilities;
4. create a bounded local support session;
5. run read-only diagnostics with real observations;
6. explicitly approve state-changing actions;
7. revoke the session;
8. operate entirely without a Dev11 cloud service.

## S0 — current platform model

**Substantially implemented**

- policy/grants/sessions;
- tasks and observations;
- route selection;
- semantic API models;
- identity scaffolding;
- remote-access/pairing architecture;
- hardware/HID prototype code.

## S1 — ephemeral local Agent — achieved baseline

Run:

```text
relmote serve
```

Relmote starts a localhost service and browser UI.

Initial capabilities should be deliberately narrow and useful:

- system identity;
- OS/platform information;
- hostname;
- CPU/memory summary;
- network-interface inspection;
- disk/filesystem summary;
- process/service summary where portable;
- read-only diagnostics.

No arbitrary remote shell is required for S1.

### Deployment forms

Support, in order:

1. Python package/development install;
2. single command / ephemeral environment;
3. packaged standalone executable;
4. OS-native packages/services later.

## S2 — local web/PWA controller

Responsive controller for phone/tablet/desktop browser.

Show:

- node;
- target;
- capabilities;
- session/mode;
- observations;
- proposed actions;
- revoke.

Default binding remains localhost until authentication/pairing is implemented.

## S3 — pairing + LAN access

Add reviewed controller/node key agreement and explicit local pairing.

Then permit authenticated LAN access.

No unauthenticated `0.0.0.0` support UI.

## S4 — state-changing native actions

Add a small capability-gated action set.

Examples:

- controlled service restart;
- network configuration change;
- bounded file write.

Avoid exposing a universal shell merely because it is easy.

## S5 — installed Agent

Persistent `relmoted` service with:

- stable node identity;
- owner/controller trust;
- OS service integration;
- conservative updates;
- local-first operation.

## S6 — temporary support invitation

Create an expiring one-time support relationship.

Existing VPN/direct IP can provide reachability initially.

## S7 — native remote access

Direct P2P/rendezvous/encrypted relay after pairing/session semantics are stable.

## S8 — Relmote Live

Bootable recovery environment implementing the same node/API model.

## Hardware track H1 — physical HID bench

In parallel when hardware is available:

- Pi Zero 2 W-class prototype;
- AUTHORIZE;
- STOP;
- USB HID.

The code and bring-up plan already exist.

## Hardware track H2 — hybrid

Hardware node discovers software Agent on the target and upgrades the same task from physical HID/KVM to native capabilities.

## Later

- serial module;
- KVM;
- Pocket custom hardware;
- mesh/store-and-forward;
- additional native management plugins.

## Current relationship to the project

The S1/S2 baseline has been surpassed by the active Linux preview. Current work includes remote-support sessions, Agent Access/Agent Host pairing, screen-provider integration, richer workspace operations, and continued hardware validation.

Hardware work continues as a parallel track rather than the gate to software deployment.

See [STATUS.md](STATUS.md) for what is actually implemented now.
