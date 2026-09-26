# Relmote All-in-One — reference concept

**Goal:** a pocketable/power-bank-sized Relmote that carries the most common field interfaces without requiring a bag of modules.

The All-in-One is not a “better” Relmote tier. It is a different physical configuration.

## Character

Think:

- rugged power bank;
- compact field computer;
- thicker than Pocket;
- still coat-pocket / small-bag friendly.

## Candidate integrated capabilities

Potentially:

- Linux compute;
- independent safety MCU;
- Wi-Fi;
- BLE;
- battery;
- multiple USB-C ports;
- Ethernet;
- serial transceiver;
- KVM/video capture;
- microSD/removable storage;
- one low-power long-range radio slot or module bay;
- small status display;
- AUTHORIZE and STOP.

Not every item must be built in. The point is to make the common field configuration self-contained.

## Concept

```text
╭──────────────────────────────╮
│ RELMOTE                      │
│                              │
│ target: thinkpad             │
│ system: USB HID + HDMI       │
│ controller: BLE              │
│ mode: ASSIST                 │
│ battery: 74%                 │
│                              │
│ [ AUTHORIZE ]        [ STOP ]│
├──────┬──────┬───────┬────────┤
│USB-C │USB-C │ ETH   │ SERIAL │
╰──────┴──────┴───────┴────────╯
```

## Expansion

All-in-One should still expose the open module/USB-C expansion model.

Integrated hardware must not imply a closed SKU.

## Repairability

Likely internal replaceable assemblies:

- battery;
- I/O daughterboard;
- compute board;
- safety/radio board;
- display;
- antenna subassemblies where practical.

## Power

The larger enclosure may support:

- larger replaceable battery;
- higher USB-C input power;
- intentional power-bank output mode;
- dock/PoE operation.

Power output must remain logically separate from target-control authorization.
