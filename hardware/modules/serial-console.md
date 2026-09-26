# Serial / Console module

**Likely class:** S

## Purpose

Turn Pocket into a field console for routers, switches, embedded systems, and appliances.

## Variants

Potentially separate or configurable:

- 3.3 V TTL UART;
- 5 V-tolerant UART where safely designed;
- RS-232;
- RS-485;
- RJ45 console;
- isolated industrial variant.

## Capabilities

```text
serial.rx
serial.tx
observe.console
```

Electrical mode should be reported explicitly.

## Safety

Never guess target voltage.

A module should support:

- voltage sensing where feasible;
- clear labeling;
- configurable level shifting;
- overvoltage protection.

## Why module?

Legacy/industrial electrical interfaces consume connector/board space and vary dramatically.

The base Pocket should not expose raw pins merely to claim universality.
