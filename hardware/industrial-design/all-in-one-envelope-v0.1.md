# Relmote All-in-One envelope v0.1

**Status:** provisional reference envelope.

## Overall reference

Initial target:

```text
height:    155 mm
width:      78 mm
thickness:  28 mm
corner R:    9 mm nominal
```

This puts the All-in-One firmly in **compact power-bank / field-instrument** territory while still fitting a coat pocket or small bag.

## Why thicker?

The extra 10 mm over Pocket makes room for:

- larger/serviceable battery;
- Ethernet jack;
- video capture hardware;
- greater thermal mass;
- more replaceable daughterboards;
- optional cylindrical-cell design studies;
- stronger module/dock mechanics.

## Candidate face layout

```text
╭──────────────────────────────╮
│ RELMOTE                      │
│                              │
│       larger status UI       │
│                              │
│ target / path / mode / power │
│                              │
│ [ AUTHORIZE ]        [ STOP ]│
├──────────────────────────────┤
│ target USB-C   power USB-C   │
│ HDMI IN        Ethernet      │
╰──────────────────────────────╯
```

The exact port set is not frozen.

## Battery direction

Unlike Pocket, All-in-One has enough thickness to study:

- replaceable flat battery pack;
- one or more standard cylindrical cells;
- swappable external battery sled.

A standard-cell design is attractive for repairability, but cell protection, mechanical retention, runtime, and enclosure efficiency must be tested before choosing it.

## Modular compatibility

All-in-One should still expose:

- standard USB-C expansion;
- Relmote module compatibility where physically practical;
- docking.

Integrated interfaces are convenience, not exclusive access to capabilities.

## Service architecture

Prefer distinct replaceable boards for:

- high-wear USB-C;
- Ethernet/HDMI;
- radios;
- compute;
- safety MCU;
- battery/power path.

This form factor should be easier to repair than Pocket, not merely contain more components.
