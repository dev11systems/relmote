# Embedded Debug module

**Likely class:** S

## Purpose

Authorized development/debug access for owned lab hardware.

Potential interfaces:

- SWD;
- JTAG;
- UART;
- GPIO;
- I²C;
- SPI;
- target voltage sense.

## Capabilities

Examples:

```text
debug.swd
debug.jtag
gpio.read
gpio.write
bus.i2c
bus.spi
firmware.read
firmware.write
```

Dangerous write/debug capabilities remain explicit grants.

## Electrical safety

The module should:

- detect/reference target voltage;
- avoid blindly driving unknown rails;
- provide level shifting;
- consider isolation variants.

## Why module?

These interfaces are extremely useful to makers/engineers but unnecessary for ordinary IT support.
