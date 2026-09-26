# Pocket board map v0.1

A first conceptual board decomposition:

```text
 FRONT
╭─────────────────────────────────╮
│ Display / Controls Board        │
│ AUTHORIZE   indicators   STOP   │
├──────────────────┬──────────────┤
│                  │ Compute PCB  │
│ Battery region   │              │
│                  ├──────────────┤
│                  │ Safety PCB   │
├──────────────────┴──────────────┤
│ Power / USB-C I/O Daughterboard │
╰─────────────────────────────────╯
 REAR
┌─────────────────────────────────┐
│ Replaceable Module Contact PCB  │
└─────────────────────────────────┘
```

This is not intended to imply five PCBs are optimal.

## Prototype board-count options

### Option A — maximum separation

5 boards:

1. display/control;
2. compute;
3. safety;
4. power/I/O;
5. module contact.

Best for learning and replacement, worst for connectors/cost.

### Option B — likely Pocket compromise

4 boards:

1. display/control;
2. compute;
3. safety + power management;
4. I/O + module-contact assemblies separated by flex/cable.

Potential issue: combining safety and power increases trusted-board complexity.

### Option C — likely production simplification

3 boards:

1. main compute/power board;
2. independent safety + physical-control board;
3. replaceable I/O/contact board(s).

Best cost/space, but repair fault domains become coarser.

## Current preference

For development:

> **keep safety physically separate and make ports/contact surfaces replaceable.**

Do not optimize PCB count until failure/testing data exists.
