# USB-C / power-path study v0.1

Relmote's power architecture is unusually important because the device may simultaneously be:

- charging;
- powered from a target;
- connected to a controller;
- powering modules;
- optionally sourcing power.

## Reference architecture

```text
USB-C POWER/CTRL ─┐
                  ├─► protected power-path / charger ─► system rail
battery ──────────┤                              │
module battery ───┘                              ├─► core
                                                 ├─► modules
TARGET USB-C ─── data isolation/role logic ──────┘
```

Exact topology remains open.

## USB-C Power Delivery

USB-C PD is attractive for:

- charging;
- high-current external power;
- dock operation;
- optional intentional power-bank output.

A controller/charger combination can support negotiated bidirectional source/sink behavior, but Relmote should use this deliberately rather than make every port dual-role by default.

## Port roles

### POWER / CTRL

Candidate roles:

- PD sink;
- optional PD source;
- USB controller/service data;
- firmware recovery.

### TARGET

Default philosophy:

- target-facing data;
- conservative power role;
- never infer authorization from cable attach.

### EXPANSION

Optional:

- USB host;
- dock;
- external high-speed module.

## Power-path IC requirements

Production selection should support:

- battery charging;
- system power while charging;
- input current limiting;
- thermal regulation;
- battery temperature input;
- reverse-current protection;
- source/sink state reporting;
- ship/storage mode;
- MCU/host telemetry.

## Prototype path

Do not design the production PD board first.

Use known development modules / SBC power for v0.1 HID bench testing.

Build a dedicated power-path evaluation board before integrating Pocket PCB.

## Safety

Power-bank functionality is optional and must never automatically enable a data path.

The UI should display both:

```text
POWER ROLE: source/sink
DATA ROLE: controller/target/none
```

because USB-C makes these conceptually easy to confuse.
