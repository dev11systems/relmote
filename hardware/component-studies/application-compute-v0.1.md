# Application compute study v0.1

Relmote Pocket needs enough compute for protocol/routing/UI/networking and modest local intelligence, but should not optimize around continuous heavy AI inference.

## Candidate classes

### Class A — high-performance 55 × 40 mm compute modules

Examples:

- Raspberry Pi Compute Module 5 class;
- RK3588-class compute modules.

Strengths:

- excellent Linux ecosystem;
- substantial CPU;
- high-speed interfaces;
- enough RAM for meaningful local models;
- existing module ecosystem.

Weaknesses for Pocket:

- power/thermal behavior pushes against long battery life;
- consumes a large fraction of the internal planar area;
- may require substantial heat spreading;
- makes the base product more expensive/powerful than many Relmote tasks require.

**Position:** excellent prototype / All-in-One / accelerator candidate; keep under consideration for Pocket but do not make it the baseline assumption.

### Class B — efficient embedded Linux SOM

Examples:

- i.MX 8M Mini/Nano class;
- RK3566-class;
- future efficient Cortex-A55/A53 SOMs.

Strengths:

- Linux-capable;
- lower performance/power target;
- mature embedded interfaces;
- USB OTG;
- smaller SOMs exist;
- often stronger product-lifecycle focus.

Weaknesses:

- fragmented vendor BSP quality;
- some GPU/NPU stacks are less open;
- smaller community than Raspberry Pi;
- certified Wi-Fi/BLE may depend on SOM variant.

**Position:** currently the most architecturally natural Pocket class.

### Class C — very low-power embedded Linux

Examples:

- i.MX 6ULL-class;
- similar Cortex-A7/A35-class parts.

Strengths:

- excellent idle/suspend potential;
- low thermal burden;
- long product life.

Weaknesses:

- limited local AI;
- lower UI/browser performance;
- may constrain future protocol/crypto workloads.

**Position:** compelling for Mini/low-power node variants, potentially too constrained for the flagship Pocket.

### Class D — custom application-processor board

Strengths:

- best packaging;
- best power optimization;
- only interfaces we need;
- potentially lowest production thickness.

Weaknesses:

- highest engineering burden;
- DDR/high-speed layout complexity;
- harder DIY repair;
- greater certification/support burden.

**Position:** production optimization after requirements stabilize, not v0.1.

## Reference data points

### Raspberry Pi Compute Module 5

Published envelope:

```text
55 × 40 × 4.7 mm
```

Typical documented power:

```text
idle:       ~400 mA @ 5 V ≈ 2 W
operating:  ~900 mA @ 5 V ≈ 4.5 W
```

These figures vary with workload/software.

This is feasible inside Pocket physically, but a ~2 W compute-module idle before display, radios, safety plane, and power conversion is substantially above our desired connected-idle target.

### i.MX 8M Mini class

The SoC provides:

- quad Cortex-A53;
- Cortex-M4;
- two USB 2.0 OTG controllers;
- Linux support;
- Gigabit Ethernet MAC;
- PCIe.

Commercial SOMs exist around:

```text
55 × 30 mm
```

Measured third-party embedded-module examples show roughly ~1.2–1.9 W idle depending on configuration, with deep/suspend states much lower.

This class still requires careful suspend design but is directionally closer to Pocket.

### RK3566 class

Provides:

- quad Cortex-A55;
- USB OTG;
- PCIe;
- modest NPU on some implementations;
- Linux community support.

Interesting as a middle ground, but software openness/BSP quality must be evaluated per module.

## Pocket recommendation — v0.1

Do **not** select the production compute module yet.

Prototype software on Pi Zero/other readily available boards.

For the physical Pocket architecture, reserve approximately:

```text
~55 × 40 mm maximum compute-module envelope
≤ ~7 mm local board-stack height
```

but actively search for a smaller/lower-power SOM.

## All-in-One recommendation

CM5/RK3588-class compute is much easier to justify in the 28 mm All-in-One envelope, especially if:

- larger battery;
- heat spreader;
- optional active cooling/dock;
- local AI/KVM/video processing

are desired.

## Production selection gate

Before freezing Pocket compute, measure candidates for:

1. cold boot;
2. suspend/resume;
3. idle with radios;
4. USB gadget active;
5. BLE controller active;
6. Wi-Fi transfer;
7. light local model;
8. thermal rise inside representative enclosure;
9. mainline/upstream driver dependence.
