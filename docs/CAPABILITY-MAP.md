# Relmote capability map

The use-case atlas is broad. The core platform should remain small.

This document maps recurring needs into reusable capability families.

## Principle

A use case should usually be composed from:

```text
controller transport
+ system transport
+ observation type
+ capability grant
+ optional module
+ optional planner
```

rather than implemented as a bespoke “mode.”

## Core capability families

### Node / identity

- node identity;
- pairing;
- controller identity;
- target identity;
- session identity;
- discovery;
- path state.

**Placement:** base software.

### Authorization / safety

- Observe / Teach / Assist / Operate;
- capability grants;
- expiry;
- physical AUTHORIZE;
- STOP/revoke;
- replay protection;
- audit metadata.

**Placement:** base Pocket + safety plane + base software.

### Human-interface output

- keyboard;
- pointer;
- future touch/gamepad/specialized HID where justified.

**Placement:** base Pocket for keyboard; additional forms may be software/firmware extensions.

### Text console

- USB CDC;
- UART;
- RS-232;
- RS-485;
- SSH;
- other authenticated shells.

**Placement:** USB/SSH software in core; electrical legacy interfaces in modules.

### Visual

- screen observation;
- KVM;
- video capture;
- OCR/vision as optional interpretation above raw frames.

**Placement:** KVM module / All-in-One.

### Network-native management

- SSH;
- HTTPS/device APIs;
- Redfish;
- platform management APIs.

**Placement:** software plugins; physical Ethernet may be module/All-in-One.

### Out-of-band management

- KVM;
- serial;
- BMC/Redfish;
- AMT-class interfaces where configured.

**Placement:** mix of modules and software.

### File / storage

- read/write files through authorized native paths;
- removable recovery media;
- evidence storage.

**Placement:** core software + optional storage/recovery modules.

### Radio / constrained transport

- LoRa;
- MeshCore;
- Meshtastic;
- 802.15.4/Thread/Zigbee where useful;
- cellular;
- satellite/external modem.

**Placement:** mostly modules/plugins.

### Power

- battery telemetry;
- USB-C PD;
- module power budgeting;
- target power state;
- optional intentional power-bank output;
- PoE through dock/module.

**Placement:** base power plane + modules.

### Embedded/debug

- UART;
- GPIO;
- I²C;
- SPI;
- SWD/JTAG.

**Placement:** explicit development modules/plugins.

### Task/evidence

- durable task;
- proposal;
- approval;
- observation;
- evidence provenance;
- semantic compression;
- store-and-forward.

**Placement:** base software.

## Placement test

For each capability ask:

### Must every Pocket have it?

If yes, consider base hardware.

### Is it electrically bulky, high-power, certification-heavy, or niche?

If yes, prefer module.

### Is it only a protocol/driver?

Prefer software plugin.

### Is it commonly useful in field support and benefits from native ports?

Consider All-in-One integration.

## Example decomposition

### Family laptop support

```text
BLE controller
+ USB HID
+ KVM module
+ Assist grant
+ screen observations
+ optional remote planner
```

### Router recovery

```text
BLE or mesh controller
+ serial module
+ text observations
+ Assist/Operate grant
+ optional semantic summarizer
```

### Homelab server

```text
LAN controller
+ SSH/Redfish plugins
+ optional KVM
+ structured/text observations
+ long-lived docked power
```

### Embedded bench

```text
USB controller
+ debug module
+ UART/SWD
+ explicit firmware/debug capabilities
+ human/manual planner
```

The same platform primitives cover very different scenarios.
