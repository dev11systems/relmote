# Module interconnect study v0.1

Relmote's snap system needs two very different electrical jobs:

1. durable low/moderate-speed service contacts;
2. optional high-speed interconnect.

Trying to solve both with one generic pogo array is unnecessary.

## Service contacts

Pogo/spring contacts remain a strong candidate for:

- power;
- ground;
- presence;
- control;
- UART;
- interrupt;
- modest-speed links;
- potentially USB 2.0 after validation.

Benefits:

- exposed mating surface can remain flush/recessed;
- easy module attachment;
- no insertion motion;
- field-cleanable;
- replaceable contact board.

Framework's Laptop 16 development is a useful precedent: after an earlier spring-contact design proved vulnerable to bending, it moved to a custom pogo solution for high-cycle modular input connectors, reporting a 10,000-cycle rating for the pins used there.

That does not validate our electrical design, but it supports the mechanical concept.

## Contact board

Pocket should place pogo/spring hardware on a **replaceable rear contact PCB**, not the mainboard.

This turns contact wear/damage into a service operation.

## USB 2.0

USB 2.0 over spring contacts may be possible, but it must be validated with:

- impedance-aware routing;
- return paths;
- ESD;
- eye/signal testing;
- stack/module geometry.

Until tested, the module spec should continue saying **optional USB 2.0**, not guaranteed USB 2.0.

## High-speed layer

For USB 3/USB4/DisplayPort/PCIe/video-class links, use a purpose-designed connector/interposer.

Candidate categories:

- compact board-to-board mezzanine;
- compression interposer;
- recessed standard USB-C mating scheme;
- other openly purchasable high-speed connector.

Selection criteria:

- bandwidth;
- cycle life;
- alignment tolerance;
- repairability;
- vendor availability;
- hobbyist accessibility;
- cost;
- thickness.

## Hybrid USB-C snap

This remains particularly attractive:

```text
magnets + rail  → alignment/mechanical load
recessed USB-C  → standard electrical interface
```

Potential advantages:

- standardized electrical behavior;
- commodity cables/adapters remain conceptually compatible;
- high-speed validation burden moves toward a known connector.

Potential disadvantages:

- USB-C plug/receptacle geometry may be awkward for zero-insertion-force snap behavior;
- connector cycle/alignment forces;
- role/orientation logic;
- mechanical tolerance.

We should prototype this rather than assume it wins.

## Mechanical test fixture

Before freezing module geometry, build a simple fixture for:

- repeated attach/remove cycles;
- shear load;
- pull force;
- drop/shock;
- contamination/dust;
- contact resistance;
- misalignment;
- module stack bending.

## Recommendation

Use **pogo/spring contacts for the service plane** in the first physical module prototype.

Keep high-speed electrical transport separate until a real KVM/high-speed module forces the decision.
