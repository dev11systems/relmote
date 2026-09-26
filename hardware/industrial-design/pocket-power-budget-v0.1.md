# Relmote Pocket power/runtime study v0.1

**Status:** rough engineering budget, not measured product data.

This document intentionally uses **ranges** because no application processor, display, radio chipset, or battery has been selected.

## Battery study

A phone-sized replaceable pack in the current envelope might plausibly land in the broad neighborhood of:

```text
15–25 Wh
```

depending on:

- cell chemistry;
- thickness;
- safety margins;
- connector/retention;
- internal board area;
- desired serviceability.

This is a packaging target only.

## Core power states

### Deep/standby

Target architectural goal:

```text
~0.1–0.5 W
```

May require the Linux application processor to sleep/off while the safety MCU or low-power controller remains awake.

### Connected idle

Rough design target:

```text
~0.7–1.5 W
```

Includes low-power compute state, BLE/Wi-Fi management, display/status, and safety plane.

### Typical interactive

Rough design target:

```text
~2–4 W
```

Examples:

- local web/phone control;
- USB HID/serial;
- moderate networking;
- light local reasoning/processing.

### Heavy local compute

Could easily exceed:

```text
5–10+ W
```

depending on processor/accelerator.

Pocket should not be architected around continuous heavy AI inference unless testing proves the thermal/battery tradeoff acceptable.

Cloud/phone/home-server intelligence exists specifically so Pocket can remain efficient.

## Illustrative runtime

Ignoring conversion losses and reserve margins, a 20 Wh pack gives:

| Average load | Idealized runtime |
| ---: | ---: |
| 0.25 W | 80 h |
| 0.75 W | 26.7 h |
| 1 W | 20 h |
| 2 W | 10 h |
| 3 W | 6.7 h |
| 5 W | 4 h |
| 8 W | 2.5 h |

Real runtime will be lower.

The useful lesson is architectural: **idle efficiency matters more than peak performance** for a device that may wait attached to a system for hours.

## Module budgets

Illustrative only:

```text
LoRa/mesh:      low average, bursty transmit
GNSS:           low/moderate continuous
cellular:       moderate average, high burst
KVM capture:    moderate/high continuous
Ethernet:       moderate
extra compute:  potentially high
```

Every module descriptor already has fields for typical and peak power.

Relmote should use those values for admission control.

## Charging

Pocket should support operation while externally powered.

USB-C power input should be sized so that Relmote can:

- run the core;
- charge the battery;
- power ordinary modules;

without assuming that every source can do all three simultaneously.

The system should expose:

```text
input power available
core load
module load
battery charge/discharge
thermal charge limit
remaining downstream budget
```

## Target power

Target-provided USB power may be useful for lightweight operation, but it should not be assumed sufficient for:

- fast charging;
- KVM;
- cellular transmit peaks;
- large module stacks.

Target power also remains logically separate from target authorization.

## Power-bank mode

Pocket may eventually provide intentional USB-C output power.

If implemented:

- user enables it explicitly;
- UI shows source/sink state;
- data role remains independently controlled;
- target-control authorization does not follow power role;
- reserve threshold prevents draining the safety plane unexpectedly.

## Safety reserve

A future design should consider reserving enough energy for:

- safety MCU;
- STOP handling;
- clean transport shutdown;
- audit/state persistence;
- controlled USB detach.

This may be a small capacitor/reserve rail rather than a second battery.

## Design implication

Pocket's best architecture is likely:

> **efficient node first, optional local AI accelerator second**

rather than attempting to make the base device a miniature always-on GPU workstation.
