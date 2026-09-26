# Relmote Pocket internal layout v0.1

**Status:** packaging study, not a board layout.

The purpose of this document is to test whether the **150 × 72 × 18 mm** Pocket envelope can plausibly contain the architecture without sacrificing repairability.

## Usable internal envelope

The exterior is 150 × 72 × 18 mm.

After provisional allowances for:

- ~1.5 mm front shell;
- ~1.5 mm rear structural/service shell;
- ~1 mm combined internal clearance/insulation;
- perimeter wall/rib thickness;

a first-order target for the central electronics/battery stack is approximately:

```text
~144 × 66 mm planar region
~14 mm usable Z budget
```

This is intentionally conservative and must be validated in CAD.

## Don't vertically stack everything

The first enclosure sketch implied:

```text
display
compute
battery
I/O
module contacts
```

all vertically.

That is probably the wrong packaging strategy for an 18 mm device.

Instead, Pocket should use **planar zoning**:

```text
TOP
╭────────────────────────────╮
│ antenna keep-out           │
│ Wi-Fi/BLE                  │
├────────────────────────────┤
│ display/control │ compute  │
│                 │ + safety │
├─────────────────┴──────────┤
│                            │
│        BATTERY             │
│                            │
├────────────────────────────┤
│ replaceable I/O daughterbd │
│ USB-C PWR      USB-C TARGET│
╰────────────────────────────╯
BOTTOM
```

This lets the battery and electronics share the **XY area** instead of demanding impossible cumulative thickness.

## Proposed zones

Coordinates are conceptual, measured from the front view.

### Zone 1 — antenna / RF

Top ~15–20 mm.

Reserve this region from:

- large magnets;
- metal shielding directly over antenna elements;
- high-current switching inductors;
- dense high-speed connectors.

Potential antenna strategy:

- Wi-Fi/BLE antenna near top edge;
- optional diversity/secondary antenna along upper side;
- module radios use their own antenna regions and descriptors.

The final enclosure material near antennas should be RF-transparent.

### Zone 2 — display/control

Upper-left/center.

Approximate board envelope:

```text
~56 × 38 mm
```

Contains:

- display connector/driver as required;
- AUTHORIZE interface;
- STOP interface path;
- hardware safety indicators;
- optional haptic/buzzer.

The physical STOP path should route to the safety plane independently of the Linux UI.

### Zone 3 — compute + safety

Upper-right / center strip.

Initial packaging allowance:

```text
~30–36 mm wide
~55–70 mm tall
board stack target: ≤ 6–7 mm
```

This may contain:

- application processor / compute module;
- RAM/storage;
- safety MCU;
- secure/user-key storage if used;
- PMIC interfaces.

A production design may combine compute and safety on one PCB while maintaining electrical/firmware separation, or use two boards for easier iteration.

### Zone 4 — battery

Largest contiguous central/lower planar region.

Initial study target:

```text
~60–65 mm wide
~70–90 mm tall
~5–7 mm cell thickness
```

This is not a selected battery.

The design should optimize around a **replaceable pack envelope**, not a one-off glued pouch.

### Zone 5 — I/O daughterboard

Bottom ~15–22 mm.

Contains high-wear ports:

- POWER/CTRL USB-C;
- TARGET USB-C;
- ESD/protection;
- USB role/power-path components where appropriate.

The entire daughterboard should be replaceable without replacing the main compute board.

### Zone 6 — rear module interface

A thin rear PCB/flex/contact assembly services:

- S-ZONE A;
- S-ZONE B;
- module detect;
- switched module power;
- service bus;
- optional high-speed connector.

This assembly should be replaceable because pogo/contact surfaces are wear items.

## Z-stack study

A plausible *local* stack, not all layers across the whole device:

```text
front shell / lens             1.5 mm
display region                 2–3 mm
PCB/component region           2–5 mm
air/insulation/structure       1–2 mm
battery region                 5–7 mm
rear module-contact structure  1–2 mm
rear shell                     1.5 mm
```

Different XY zones consume different portions of the 18 mm thickness.

This is why planar zoning matters.

## Fasteners

Initial target:

- four to six perimeter screws;
- avoid screws through the battery footprint;
- rear service cover removable first;
- battery removable before main PCB;
- I/O daughterboard accessible from rear/bottom service path.

## Magnets versus internals

The rear snap magnets must be treated as **real internal components**.

Keep-outs are required around:

- battery pouch edges;
- RF antennas;
- magnetically sensitive sensors;
- inductors;
- storage/media if relevant.

The final magnet pattern cannot be chosen independently of internal packaging.

## Thermal path

Pocket should assume that sustained high compute is not its default operating state.

Thermal strategy:

```text
SoC / power components
       ↓
thermal spreader / midframe
       ↓
enclosure surfaces
```

Avoid routing heat into the center of the battery.

The battery should have:

- temperature sensing;
- thermal isolation from peak SoC/charger hot spots;
- conservative charge throttling.

## Preliminary conclusion

**150 × 72 × 18 mm still looks plausible** if:

- the design uses planar zoning rather than vertical board/battery stacking;
- Pocket does not integrate KVM/Ethernet/cellular all at once;
- the battery target remains modest;
- high-power radios and KVM remain modules;
- the compute platform is chosen for low idle/typical power rather than maximum benchmark performance.

The next validation is component-envelope CAD, not another conceptual shrink.
