# Relmote compute architecture

Relmote should not equate “intelligent” with “put the biggest AI accelerator possible in the base device.”

The Pocket form has four distinct compute roles.

## 1. Safety plane

Always local.

Responsibilities:

- physical STOP;
- output gate;
- watchdog;
- target-facing low-level enforcement;
- minimal trusted state.

Desired properties:

- deterministic;
- low power;
- fast boot;
- independent of the main application processor;
- open firmware;
- recoverable.

Likely class: MCU.

## 2. Node/control plane

Normally local.

Responsibilities:

- Relmote protocol;
- sessions;
- capability discovery;
- routing;
- audit metadata;
- module discovery;
- local UI;
- networking;
- store-and-forward.

This does **not** require a large AI model.

Desired properties:

- low idle power;
- Linux or similarly capable open environment;
- good USB support;
- Wi-Fi/BLE;
- suspend/low-power modes;
- long-term upstream support.

## 3. Planner/intelligence plane

May live anywhere:

```text
Relmote local model
phone/tablet
laptop
home server
remote GPU
cloud model
another Relmote
human
```

The protocol should make these interchangeable.

## 4. Optional accelerator

A module may add:

- NPU;
- GPU;
- larger RAM;
- specialized inference hardware.

That keeps the base Pocket efficient and affordable.

## Reference Pocket strategy

The default Pocket should optimize for:

> **always-available interface/router + modest local intelligence**

rather than:

> **always-on pocket datacenter**

A small local model may be valuable for:

- classification;
- summarization;
- command parsing;
- offline intent routing;
- safety-independent convenience;
- semantic compression for constrained links.

Heavy coding/reasoning can use a phone, home server, workstation, or cloud provider.

## Compute-module question

A physically replaceable compute module is desirable but not mandatory if it causes excessive thickness/cost.

Possible approaches to prototype:

### A. Custom mainboard + socketed compute module

Best upgradeability, hardest mechanical/electrical design.

### B. Replaceable entire compute PCB

Simpler and still repairable.

The main PCB is a service part, while battery/I/O/module contacts remain separate.

### C. Standard SOM

Potentially attractive if an open, long-lived SOM meets:

- size;
- power;
- USB requirements;
- availability;
- documentation.

No SOM standard is selected yet.

## Software portability

The node/control plane should minimize hardware-specific code.

Platform adapters should isolate:

- GPIO;
- USB gadget;
- Bluetooth;
- power management;
- display;
- module bus.

That makes it realistic to support:

- Pi prototypes;
- ARM production hardware;
- x86 DIY builds;
- RISC-V experiments;
- future boards.

## Offline behavior

Relmote without Internet should still support:

- manual operation;
- local companion control;
- stored tasks;
- HID/serial/network transports;
- module discovery;
- safety/policy;
- local logs.

Cloud AI must never be required for basic ownership or administration.

## Design rule

**The safety plane must not depend on the planner/intelligence plane being correct, online, responsive, or even present.**
