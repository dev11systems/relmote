# Modularity

Relmote is one platform with many possible physical implementations.

The platform should not be defined by one PCB, enclosure, connector, radio, operating system, or AI provider. The durable layer is the combination of:

- Relmote protocol;
- capability model;
- authorization model;
- transport abstraction;
- module discovery;
- open hardware interface conventions.

A tiny MCU board, a phone-sized pocket unit, a power-bank-sized all-in-one device, and a large field station can all be Relmote-compatible.

## Design goals

Relmote modularity should be:

- **optional** — the core remains useful without modules;
- **open** — third parties can build compatible hardware without permission;
- **repairable** — wear items and batteries should be replaceable;
- **discoverable** — modules announce what they can do;
- **transport-neutral** — modules expose capabilities, not product-specific assumptions;
- **gracefully degradable** — removing a module removes capabilities, not the whole system;
- **physically robust** — magnets may align/retain, but the enclosure geometry should carry shear loads;
- **standard-friendly** — USB-C and ordinary external adapters remain first-class paths.

## Three extension paths

Relmote should support multiple extension mechanisms rather than forcing everything through one proprietary bus.

### 1. Snap modules

For compact integrated accessories.

```text
Relmote Core
     ║
magnetic/keyed interface
     ║
LoRa / battery / GNSS / serial / sensors
```

The snap interface may provide:

- power;
- module presence;
- low-speed control;
- moderate-speed data;
- optional USB 2.0;
- optional pass-through.

### 2. High-speed snap modules

Modules that need video capture, high-speed networking, or other demanding links may engage an additional high-speed connector.

The high-speed connector is optional. A simple radio or battery module should not need expensive signal-integrity hardware just to participate in the ecosystem.

### 3. Standard external modules

USB-C remains the universal escape hatch.

```text
Relmote ── USB-C ── arbitrary external hardware
```

A device does not need to use the magnetic module system to be Relmote-compatible.

## Mechanical philosophy

The reference magnetic system should use:

- magnets for alignment and light retention;
- keyed geometry to prevent incorrect orientation;
- a shallow rail, lip, latch, or equivalent feature to carry shear loads;
- recessed contacts;
- no exposed sharp edges;
- published mechanical CAD;
- published magnet locations and polarity;
- published mating tolerances.

The magnetic system is a reference implementation, not a requirement for Relmote compatibility.

## Stackability

Some modules may support downstream modules.

```text
Core
 ├─ Mesh
 ├─ Cellular/GNSS
 └─ Battery
```

Each module should advertise pass-through properties, for example:

```yaml
passthrough:
  power: true
  control: true
  usb2: true
  high_speed: false
```

Stacking should remain bounded by:

- power budget;
- thermal budget;
- mechanical stability;
- bus topology;
- signal integrity;
- transport conflicts.

A module that cannot safely pass a resource must explicitly terminate it.

## Capability discovery

Modules should describe capabilities rather than forcing the main software to know every product SKU.

Example:

```yaml
module:
  id: dev11.mesh.lora.v1
  hardware_revision: 1
  firmware_revision: 3

capabilities:
  - radio.lora
  - mesh.meshcore
  - mesh.meshtastic

power:
  typical_mw: 450
  peak_mw: 1800

links:
  - control
  - usb2

passthrough:
  power: true
  control: true
```

The exact descriptor encoding remains part of the module specification.

## Repairability

Reference hardware should prefer:

- screws over adhesives;
- replaceable batteries;
- replaceable I/O/port daughterboards;
- replaceable compute modules where practical;
- standard fasteners;
- labeled boards and connectors;
- accessible test points;
- published schematics and board files;
- multiple-source components where practical;
- no serialized replacement parts;
- no cloud activation.

Ports are wear items and should be isolated on replaceable daughterboards where feasible.

## Moddability and owner control

Reference hardware should expose documented development/recovery paths, potentially including:

- UART console;
- SWD/JTAG pads;
- I²C;
- SPI;
- GPIO;
- power rails;
- module bus;
- USB recovery.

Security should not depend on locking the owner out.

If secure boot is supported, the long-term goal is **owner-controlled secure boot**: the user can choose official firmware, their own signed fork, or recovery firmware without requiring a Dev11 signing service.

## Open-hardware deliverables

A production-quality open Relmote design should publish:

- KiCad schematics and PCB layout;
- fabrication outputs;
- BOM and substitutions;
- firmware and bootloader source;
- mechanical CAD in editable and interchange formats;
- enclosure source files;
- assembly instructions;
- module-bus specification;
- repair documentation;
- test procedures;
- diagnostic tools;
- reference modules.

## Compatibility, not certification lock-in

“Relmote-compatible” should describe protocol/capability compatibility.

Dev11 may eventually publish conformance tests, but compatibility must not depend on purchasing a proprietary license, identifier, or cryptographic blessing from Dev11.
