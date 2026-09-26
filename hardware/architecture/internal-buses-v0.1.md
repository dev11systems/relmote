# Internal buses v0.1

**Status:** architecture draft. Connector families and exact electrical levels remain open.

Relmote's internal links should be intentionally narrow.

## Trust map

```text
UNTRUSTED / NETWORK-FACING
         │
         ▼
   COMPUTE PLANE
         │
         │ authenticated action protocol
         ▼
    SAFETY PLANE
         │
         ▼
      TARGET
```

The compute plane is treated as potentially compromised from the safety plane's perspective.

## Compute ↔ safety link

### Requirements

- bidirectional;
- simple;
- bounded messages;
- integrity/authentication;
- replay resistance;
- watchdog/heartbeat;
- no raw memory sharing required;
- recoverable after either side resets.

### Physical candidates

For early hardware:

- UART;
- USB device link;
- SPI.

UART is attractive for v0.x because it is:

- easy to inspect;
- easy to isolate;
- easy to recover;
- broadly supported;
- fast enough for action/control messages.

The protocol should not depend on UART permanently.

### Safety command vocabulary

The safety MCU should accept narrow commands such as:

```text
IDENTIFY_SESSION
ARM_LEASE
TYPE_TEXT
RELEASE_ALL_KEYS
DISARM
QUERY_STATE
```

It should **not** accept arbitrary HID reports from Linux by default.

That preserves semantic enforcement below the AI/node plane.

## Compute ↔ power

Preferred logical interface:

```text
telemetry + requests
```

Potential physical buses:

- I²C/SMBus;
- UART;
- dedicated GPIO interrupts.

Compute may request:

- charge policy;
- module rail enable;
- power-bank mode;
- telemetry.

The power controller remains responsible for electrical limits.

## Safety ↔ power

The safety plane should have at least one direct path to force target-output-safe state without depending on Linux.

Possible functions:

- disable target data switch;
- force target HID detach;
- assert module-output kill where applicable.

Whether STOP electrically disconnects target data remains a prototype question.

## Compute ↔ I/O board

High-speed signals may route directly between compute and the replaceable I/O daughterboard:

- USB 2/3;
- optional DisplayPort/etc.

The daughterboard may also carry:

- port role detection;
- ESD;
- load switches;
- mux/redriver components.

Avoid placing irreplaceable storage/identity solely on the wear board.

## Compute ↔ rear module board

Service-plane control should expose:

- module presence;
- descriptor discovery;
- switched power control;
- UART/control bus;
- optional USB2.

High-speed module lanes, if adopted, may route directly from compute through a purpose-designed connector.

## Debug/recovery buses

Every reference design should expose documented pads/connectors for:

- safety MCU SWD;
- compute serial console;
- power-controller debug where appropriate;
- recovery/boot straps.

These may be internal service points rather than exterior ports.

## Hot-swap matrix

| Domain | Hot-swappable while powered? | v0.1 expectation |
| --- | --- | --- |
| Snap module | intended | yes, after validation |
| External USB-C accessory | standard behavior | yes |
| Battery module | maybe | not initially |
| Internal battery | no | power down |
| I/O daughterboard | no | power down |
| Compute board | no | power down |
| Safety board | no | power down |
| Rear contact board | no | power down |

Do not advertise hot-swap merely because a connector can physically be unplugged.
