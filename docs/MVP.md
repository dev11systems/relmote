# Relmote MVP and build sequence

The platform architecture is broad. The MVP proves the central abstractions without implementing the entire atlas.

## MVP success criteria

The first meaningful prototype should prove:

1. one controller can pair with one node;
2. node identity survives transport changes;
3. target identity is explicit;
4. a bounded task becomes a proposal;
5. approval and physical authorization are distinct;
6. real target output passes through the safety boundary;
7. observations remain distinct from interpretation;
8. the same task can upgrade to a richer system path;
9. STOP/revoke works;
10. no cloud service is required.

## MVP-0 — current software model

Substantially implemented: policy, grants, sessions, replay guard, dry-run and HID transports, safety gate, task lifecycle, observations/evidence, route selection, module descriptors, power budget, and semantic API models.

## MVP-1 — physical HID bench

Pi Zero 2 W-class prototype, physical AUTHORIZE/STOP, LEDs, USB HID target, local CLI/TUI controller.

Demonstrate: propose text → approve → physically authorize → type once → STOP.

## MVP-2 — bidirectional native path

Add one text-feedback path such as SSH or USB serial/helper.

Demonstrate blind HID → richer path appears → same task re-routes → actual observation returned.

## MVP-3 — local controller UI

Build a responsive web/PWA controller first. It is cross-platform, validates the semantic API, and avoids app-store dependency. Native BLE discovery can follow.

## MVP-4 — Agent

Run relmoted directly on Linux and demonstrate software-only Relmote with pairing, identity, read-only diagnostics, optional shell, and the same controller UI.

## MVP-5 — hybrid

Pocket discovers Agent on the target. Demonstrate physical path → native upgrade → Agent disappears → physical fallback remains.

## MVP-6 — first module

Serial/console is likely the best first module: useful, bidirectional, technically tractable, and simpler than KVM.

## MVP-7 — KVM

Video capture + pointer/keyboard. This creates the strongest visual “IT support in a pocket” demonstration.

## MVP-8 — native remote access

Implement native rendezvous/direct/relay only after local identity/pairing/session semantics stabilize. Existing VPN paths can provide remote testing earlier.

## MVP-9 — constrained link

Mesh/LoRa/store-and-forward proof.

## Not MVP

Do not block early prototypes on custom Pocket PCB, final magnetic connector, cellular, custom cloud infrastructure, local large model, native iOS+Android apps, production enclosure, certification, or every module family.

## Immediate milestone

**MVP-1: real USB HID with physical AUTHORIZE/STOP on a sacrificial target.**

Architecture work should support—not indefinitely postpone—that test.
