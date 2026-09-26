# Relmote Pocket envelope v0.1

**Status:** provisional reference envelope.

## Overall dimensions

Initial target:

```text
height:    150 mm
width:      72 mm
thickness:  18 mm
corner R:    8 mm nominal
```

Why this envelope:

- unmistakably phone-sized;
- enough width for a useful display and physical controls;
- enough thickness for screws, replaceable battery, structural ribs, robust USB-C daughterboard, and module mechanics;
- still plausible in a trouser/jacket pocket;
- leaves room to get thinner later without making thinness a requirement.

## Front face

Reference layout:

```text
150 mm
╭──────────────────────────╮
│ RELMOTE                  │
│                          │
│   ┌──────────────────┐   │
│   │  status display  │   │
│   └──────────────────┘   │
│                          │
│ LINK  TARGET  MODE       │
│                          │
│ [ AUTHORIZE ]     [STOP] │
╰──────────────────────────╯
            72 mm
```

### Display window

Provisional visible window:

```text
52 × 28 mm
centered horizontally
top edge ≈ 30 mm from enclosure top
```

This is intended to accommodate roughly a **2–2.4 inch class** low-power display depending on final aspect ratio.

Display technology is intentionally not frozen. Candidates include:

- low-power monochrome/reflective LCD;
- memory LCD;
- small OLED;
- other sunlight-readable low-power panels.

E-paper remains possible for slow status surfaces but may be too slow for interaction/activity feedback.

### Information hierarchy

The physical display should be able to show, without a companion app:

```text
controller
target
controller path
system path
mode
armed/disarmed state
battery/power state
active task/action
STOP/fault state
```

The safety state must never be encoded by color alone.

## Physical controls

### AUTHORIZE

Provisional front-face control:

- left/lower region;
- approximately 20 × 9 mm tactile area;
- slightly proud or concave;
- distinct texture;
- long enough to hit deliberately with a thumb.

### STOP

Provisional front/right control:

- approximately 12–14 mm tactile diameter/area;
- physically distinct from AUTHORIZE;
- slightly recessed or guarded against pocket activation;
- still immediately reachable one-handed.

STOP should remain usable if the screen, Linux compute plane, or companion UI fails.

A later prototype may move STOP to the right side edge if one-handed testing shows that is faster and less ambiguous.

## Indicators

The display may carry most state, but at least one hardware-driven safety indicator should remain independent of the main UI.

Candidate:

- dedicated ARMED indicator adjacent to AUTHORIZE;
- dedicated STOP/fault indicator adjacent to STOP.

## Bottom edge

Initial reference:

```text
┌────────────────────────────────┐
│  USB-C POWER/CTRL   USB-C TARGET│
└────────────────────────────────┘
```

Two physically separate USB-C ports are preferred over one heavily multiplexed port.

Roles:

### POWER / CTRL

May support:

- charging/power input;
- local controller USB;
- service/recovery;
- expansion depending on negotiated role.

### TARGET

Target-facing system interface.

It should have:

- explicit physical label;
- software role enforcement;
- no automatic authority merely from attachment.

## Top edge

Candidate:

```text
USB-C EXPANSION
```

The third port is optional in the first reference design. It is useful for:

- arbitrary standard USB-C accessories;
- docking;
- external high-speed modules;
- development.

If internal complexity is too high, Pocket can ship with two USB-C ports and leave additional expansion to the snap plane.

## Side edges

Keep mostly clean for:

- grip;
- pocket insertion;
- antenna performance;
- future lanyard/strap point;
- optional hardware power switch.

Avoid fragile protruding connectors on the long sides.

## Rear face

Pocket v0.1 reserves nearly the entire rear face for the optional open snap-module system.

Reference usable zone:

```text
68 mm wide × 140 mm tall
centered on rear
```

This is divided logically into two **S zones**:

```text
╭──────────────────────╮
│      S-ZONE A        │  68 × 68 mm
├──────────────────────┤
│      4 mm seam       │
├──────────────────────┤
│      S-ZONE B        │  68 × 68 mm
╰──────────────────────╯
```

A full-size **L module** may span both zones.

See [module geometry](module-geometry-v0.1.md).

## Enclosure architecture

Reference stack:

```text
front shell
  ↓
display / control board
  ↓
compute + safety boards
  ↓
replaceable battery region
  ↓
replaceable target/I/O daughterboard
  ↓
rear structural frame + module contacts
  ↓
rear service cover
```

The design should favor:

- perimeter screws;
- captive or easily retained fasteners where practical;
- no structural adhesive;
- gasket only if later environmental goals justify it;
- battery accessible without removing the display.

## Battery envelope

Pocket should target a replaceable **pouch-style Li-ion/Li-poly battery pack** or similarly flat serviceable battery rather than force cylindrical cells into an 18 mm body.

Final capacity is not frozen.

The battery should:

- use a connector rather than soldered flying leads where practical;
- be mechanically retained without permanent adhesive;
- have clear replacement specifications;
- remain available as a generic/standardizable pack if possible.

## Internal serviceability

Preferred replaceable units:

1. battery;
2. USB-C/I/O daughterboard;
3. display/control board;
4. compute board;
5. safety MCU board where not integrated;
6. rear module-contact board.

## Surface/material direction

Reference design should prioritize:

- matte surfaces;
- impact-tolerant polymer and/or metal structural frame;
- no glossy glass back;
- tactile labels/embossing where useful;
- visible screw/service logic rather than pretending the object is seamless.

The industrial design should communicate **tool, node, field instrument** rather than luxury phone.
