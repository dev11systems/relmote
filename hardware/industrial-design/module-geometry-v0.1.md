# Relmote snap-module geometry v0.1

**Status:** exploratory mechanical envelope, not a frozen module standard.

The goal is to support both compact modules and full-back modules without making the Pocket core larger.

## Rear active area

Pocket core reference rear active area:

```text
68 × 140 mm
```

Logical division:

```text
68 × 68 mm  S-ZONE A
4 mm seam
68 × 68 mm  S-ZONE B
```

## Module classes

### S module

Reference envelope:

```text
68 × 68 mm
thickness: application-dependent
typical target: 4–10 mm
```

Examples:

- LoRa / MeshCore / Meshtastic radio;
- GNSS;
- serial/RS-232;
- sensor/interface module;
- modest battery extension.

Two S modules may occupy the rear plane simultaneously: one in each zone.

### L module

Reference envelope:

```text
68 × 140 mm
typical target: 5–14 mm
```

Examples:

- large battery;
- KVM/video;
- cellular + GNSS;
- compute accelerator;
- dock interface;
- combination module.

An L module spans both S zones.

## Stacking

A module may expose a downstream snap surface.

Reference expectation:

```text
Pocket core       18 mm
S radio module   + 6 mm
battery module   +10 mm
-----------------------
field stack       34 mm
```

A 30–35 mm stack is no longer “phone thin,” but remains roughly power-bank/field-tool territory.

Software should surface total topology, power, and thermal constraints before enabling high-load modules.

## Attachment

Each S zone should eventually provide:

- at least two magnetic alignment/retention locations;
- keyed anti-rotation geometry;
- anti-shear rail/lip;
- one service contact region.

An L module may use all attachment features from both zones.

### Magnets

Magnet size, grade, polarity, and exact coordinates remain open until:

- pull-force testing;
- shear/drop testing;
- compass/magnetometer testing;
- antenna interaction testing;
- card/media safety evaluation;
- enclosure thickness studies.

The final polarity pattern must be published.

## Service contact zone

Provisional concept per S zone:

```text
recessed service island
~24 × 10 mm
~12 spring/contact positions
```

Potential logical resources:

- multiple GND;
- module power;
- presence/detect;
- wake/interrupt;
- control;
- UART;
- optional USB 2.0;
- reserved pins.

The exact pin count/pitch is **not frozen**.

## High-speed connection

Do not force multi-gigabit signaling through generic pogo contacts.

A separate recessed high-speed connector may sit near the center seam and be engaged by:

- L modules;
- selected high-speed S modules if mechanically practical.

Candidate technologies must be evaluated for:

- open availability;
- insertion-cycle life;
- signal integrity;
- repairability;
- cost;
- hobbyist accessibility.

Standard USB-C remains the fallback when a snap high-speed interface is unnecessary or too complex.

## Hybrid USB-C snap module

Some modules may use:

- magnets + keyed enclosure geometry for mechanical retention;
- a recessed/board-mounted USB-C mating interface for standardized data/power.

This is a legitimate module class and may be preferable for certain high-speed modules.

The USB-C connector must not be expected to carry module shear loads.

## Pass-through

Stackable modules must explicitly expose which resources continue to the next layer.

A visually identical rear face must not imply electrical pass-through.

The module descriptor remains authoritative.
