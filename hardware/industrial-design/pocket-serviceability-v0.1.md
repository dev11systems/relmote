# Relmote Pocket serviceability v0.1

Repairability is a design input, not a post-release documentation exercise.

## Desired opening sequence

```text
1. power down
2. remove perimeter screws
3. lift rear service cover
4. disconnect battery
5. service I/O / module-contact / compute assemblies
```

The display should not need to be removed to replace the battery or USB-C ports.

## Replaceable assemblies

### Battery

- connectorized;
- no permanent adhesive;
- pull tab/retainer or screwed cradle;
- specification printed on pack and in docs.

### I/O daughterboard

Contains the highest-wear connectors.

Replaceable independently of:

- compute board;
- battery;
- display.

### Rear module-contact board

Pogo/contact surfaces and high-cycle mating hardware are wear components.

They should not require replacing the main PCB.

### Display/control board

Replaceable from inside after battery isolation.

### Compute board

Ideally replaceable/upgradable, though this may conflict with cost/size.

At minimum, the board should be separately replaceable rather than bonded to the enclosure.

### Safety plane

Must remain diagnosable/recoverable through a documented hardware path.

## Fasteners

Goals:

- standard Torx/Phillips/hex family;
- no proprietary driver;
- no decorative hidden clips that break during normal service;
- published screw map and lengths.

## Labels

Inside the enclosure, print/etch:

- board revision;
- connector names;
- battery polarity;
- test points;
- module bus orientation;
- recovery pins.

## Parts policy

Long-term project goal:

- publish manufacturer part numbers;
- publish acceptable substitutions;
- avoid unnecessarily single-sourced mechanical parts;
- sell replacement parts if Dev11 sells hardware;
- do not pair/serialize replacement components.

## Diagnostics

Relmote should be able to self-report:

- battery health;
- USB port status;
- module contact status;
- safety MCU status;
- thermal sensors;
- radio status;
- storage health.

Diagnostic output should be available locally without a cloud account.
