# Battery module

**Likely class:** S or L

## Purpose

Extend runtime without changing Relmote identity or software.

## Capabilities

```text
power.battery
power.telemetry
```

## Telemetry

- state of charge;
- temperature;
- health;
- design capacity;
- charge/discharge limits;
- cycle count where available.

## Architecture

The module may source the snap power rail only through negotiated power-path logic.

It must not backfeed another source unpredictably.

## Mechanical

An L full-back battery is attractive for field use.

A smaller S battery could coexist with another S module.
