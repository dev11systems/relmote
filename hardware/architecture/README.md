# Relmote hardware architecture

Relmote Pocket should be internally modular in **fault domains**, not merely assembled from multiple PCBs.

Reference domains:

```text
                    ┌─────────────────┐
                    │  Compute Board  │
                    │ Linux/node plane│
                    └────────┬────────┘
                             │
                      trusted internal
                         protocol
                             │
                    ┌────────▼────────┐
                    │  Safety Board   │
                    │ MCU / STOP / HID│
                    └────────┬────────┘
                             │
                          TARGET

 Power Board ───── system power / telemetry ─────┐
                                                 │
 I/O Board ───── USB-C / protection ─────────────┤
                                                 │
 Contact Board ─ module service plane ───────────┘
```

These may eventually be consolidated physically, but the **logical boundaries should remain**.

## Reference replaceable assemblies

### Compute board

Owns:

- application processor;
- RAM;
- primary storage;
- node/control software;
- Wi-Fi/BLE where practical;
- high-level USB/networking.

Should be replaceable without replacing:

- battery;
- safety MCU;
- external ports;
- module contacts.

### Safety board

Owns:

- safety MCU;
- physical STOP;
- AUTHORIZE lease;
- target-output gate;
- watchdog;
- hardware safety indicators;
- minimal target-facing HID path.

Should remain useful enough to force target output safe even if the compute board is dead.

### Power board

Owns:

- battery connector/protection interface;
- charger/power path;
- USB-PD power role as appropriate;
- rail generation;
- current/voltage/temperature telemetry;
- switched module power.

### I/O daughterboard

Owns wear-heavy external connectors:

- TARGET USB-C;
- POWER/CTRL USB-C;
- optional EXPANSION USB-C;
- ESD/protection components where practical.

### Rear contact board

Owns:

- spring/pogo contacts;
- module presence;
- replaceable mechanical/electrical wear surface;
- optional high-speed module connector.

## Why separate domains?

A damaged USB-C connector should not require replacing the application processor.

A worn pogo contact should not require replacing the battery.

A future compute upgrade should not require replacing the safety plane.

A crashed Linux system must not prevent STOP.

## Consolidation rule

Production cost may justify combining boards.

If two domains are placed on one PCB, preserve:

- independent power/reset where needed;
- explicit firmware boundary;
- test points;
- fault containment;
- documented logical interfaces.

Board count is an implementation detail. **Fault-domain boundaries are architecture.**
