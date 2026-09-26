# Node implementations

Relmote compatibility is behavioral, not form-factor-specific.

## Hardware nodes

- Mini — MCU-class minimal node.
- Pocket — portable phone-sized reference hardware.
- All-in-One — power-bank-sized field node.
- Docked/infrastructure — long-lived powered hardware node.

## Software nodes

- Agent — installed or ephemeral native OS service.
- Live — boot/recovery environment.
- VM — virtual machine acting as a node/gateway.
- Container — containerized node for compatible host capabilities.
- Embedded — Relmote-compatible functionality integrated into a router, appliance, SBC, or custom firmware.

## Gateway node

A node may exist primarily to bridge controller transports such as BLE, IP, mesh, or radio without itself being attached to a target.

## Composite/hybrid node

Several implementations may present one logical target experience.

```text
target laptop
├─ Agent: shell/files/logs
└─ Pocket: KVM/HID/preboot
```

The controller should not need to manually merge these capabilities.

## Compatibility

A node declares what it actually supports.

There is no requirement that every node provide physical STOP, HID, battery, screen, AI, or a module bus. Those are implementation capabilities, not platform identity.
