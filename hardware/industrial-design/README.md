# Relmote industrial design

This directory turns the platform architecture into **reference physical envelopes**.

Nothing here is production-final. Dimensions are deliberately concrete enough to prototype while remaining explicitly provisional until:

- internal board studies;
- antenna testing;
- thermal testing;
- USB-C/mechanical clearance;
- battery safety review;
- module retention testing;
- one-handed usability testing;
- pocket/bag abuse testing.

## Reference language

The current physical family is:

| Form | Reference envelope | Character |
| --- | --- | --- |
| Mini | implementation-dependent | minimal MCU/node |
| Pocket | **150 × 72 × 18 mm** | phone-sized everyday carry |
| All-in-One | **155 × 78 × 28 mm** | power-bank-sized field unit |

The envelopes are starting points, not promises.

## Pocket goals

Pocket should feel like:

- a small field instrument;
- a power bank crossed with a compact handheld computer;
- intentionally thicker than a modern phone;
- dense but not fragile;
- understandable without an app.

It should **not** feel like:

- a sealed smartphone;
- a novelty USB dongle;
- a proprietary accessory host;
- a disposable battery product.

## Current drawings/specs

- [Pocket envelope v0.1](pocket-envelope-v0.1.md)
- [All-in-One envelope v0.1](all-in-one-envelope-v0.1.md)
- [Module geometry v0.1](module-geometry-v0.1.md)
- [Design language](design-language.md)
- [Pocket front SVG](pocket-front-v0.1.svg)
- [Pocket rear SVG](pocket-rear-v0.1.svg)
- [Pocket side SVG](pocket-side-v0.1.svg)

## CAD

A simple parametric OpenSCAD envelope lives under:

`hardware/cad/pocket-envelope-v0.1.scad`

It is intentionally an **envelope model**, not a manufacturable enclosure.
