# Relmote Hardware Compatibility — Draft

Relmote compatibility describes behavior and capabilities, not ownership of a Dev11 hardware design.

## Core requirements

A hardware implementation claiming Relmote compatibility should:

1. expose a stable node identity;
2. publish capabilities;
3. distinguish controller and system transports;
4. enforce authorization before state-changing system actions;
5. provide revocation semantics;
6. avoid silently granting authority from mere physical/network connectivity;
7. represent transport limitations honestly;
8. fail closed on unknown required capabilities.

## Optional capability classes

The following classes are descriptive, not marketing tiers.

### R0 — protocol node

Can participate in the Relmote protocol and publish capabilities.

### R1 — controlled output

Can perform at least one bounded target-side action such as HID input under Relmote authorization.

### R2 — bidirectional text

Provides structured bidirectional text/console interaction.

### R3 — network-native administration

Can use native authenticated management paths such as SSH or device APIs.

### R4 — visual/KVM

Can observe visual state and provide interactive KVM-like control.

### R5 — out-of-band / autonomous edge

Supports at least one out-of-band management path and/or durable store-and-forward tasks under bounded authorization.

A device may support features from a higher class without implementing every lower-class transport.

## Capability declaration

A device should be able to describe itself in a form comparable to:

```yaml
relmote:
  protocol: 1
  class:
    - R0
    - R1
    - R2

controller_transports:
  - ble
  - wifi

system_transports:
  - usb.hid
  - usb.cdc

safety:
  physical_stop: true
  expiring_grants: true
```

## Reference hardware is not required

The following may all be Relmote-compatible:

- Dev11 Pocket hardware;
- Dev11 All-in-One hardware;
- Pi-based DIY build;
- ESP32-based DIY build;
- custom industrial node;
- large rack-mounted system;
- software-only gateway where physical output is not required.

## Open conformance

Future conformance tests should be:

- open source;
- locally runnable;
- reproducible;
- free to use;
- independent of a Dev11 cloud service.

Compatibility should not require remote activation or a proprietary certification token.
