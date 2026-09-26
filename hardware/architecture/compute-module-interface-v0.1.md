# Replaceable compute interface v0.1

Relmote should preserve the possibility of an upgradeable compute board without forcing Pocket to use a standardized SOM connector prematurely.

## Preferred v0.1 approach

Treat the **entire compute PCB as a replaceable service assembly**.

This is simpler than defining a new CPU-module standard immediately.

```text
Pocket chassis
├─ battery
├─ safety board
├─ power board
├─ I/O board
└─ COMPUTE BOARD  ← replaceable/upgradable
```

A future compute board can change SoC while preserving a small set of internal interfaces.

## Stable logical interface

A replacement compute board should ideally provide:

- system power input;
- safety link;
- power/telemetry link;
- module service link;
- target USB path;
- controller/expansion USB;
- display/control interface;
- optional high-speed module lanes;
- debug console.

## What should NOT be stable yet

Do not freeze:

- board-to-board connector;
- pin count;
- PCIe generation;
- display connector;
- exact voltage rails;
- mounting-hole pattern beyond enclosure experiments.

Those depend on real component studies.

## Upgrade philosophy

A compute upgrade should not require:

- new battery;
- new enclosure;
- new safety board;
- new module ecosystem;
- cloud reactivation.

It may require a new I/O daughterboard if a future interface standard materially changes.

## Identity

Device/user identity should not be irretrievably fused to one replaceable compute PCB.

Potential long-term locations:

- safety plane;
- replaceable secure element;
- user-controlled removable identity token;
- recoverable encrypted credentials.

No decision yet.

## DIY

The internal compute interface should be documented even if production Pocket uses a custom-shaped board.

That allows third parties to design:

- alternative ARM board;
- RISC-V board;
- high-performance board;
- ultra-low-power board;
- experimental local-AI board.

## Mechanical target

Current Pocket packaging study reserves up to approximately:

```text
55 × 40 mm
≤ 7 mm local stack height
```

for a compute assembly, but smaller is preferred.
