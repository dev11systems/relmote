# Ethernet / PoE module

**Likely class:** S or dock

## Purpose

Provide wired networking and optionally power.

Potential:

- 1 GbE;
- PoE input;
- USB-Ethernet bridge;
- dock networking.

## Capabilities

```text
network.ethernet
power.poe
```

## Why module/dock?

RJ45 thickness and magnetics consume substantial enclosure volume.

Pocket can use USB-C Ethernet externally; the snap module exists for integrated field convenience.

## PoE

PoE should be input-focused initially.

Any passthrough/source behavior requires separate power and safety analysis.
