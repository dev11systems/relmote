# Trust boundaries v0.1

Relmote should make trust boundaries explicit in both hardware and software.

## Zones

### Zone U — untrusted external

Includes:

- Internet;
- controller networks;
- Bluetooth peers;
- Wi-Fi peers;
- arbitrary USB accessories;
- third-party modules;
- target computer.

### Zone N — node/control plane

Linux/application processor.

Trusted to:

- route;
- plan;
- display;
- store;
- communicate.

Not trusted to unilaterally produce target-side output.

### Zone S — safety plane

Minimal MCU and physical controls.

Trusted to enforce:

- STOP;
- lease;
- replay guard;
- bounded action vocabulary;
- target-output gate.

Keep code and interfaces small enough to audit.

### Zone P — power plane

Electrical enforcement.

Trusted for:

- current limits;
- charging safety;
- rail isolation;
- reverse-current protection.

Software requests do not override hard electrical limits.

## Flow

```text
      Zone U
 controller / network / AI
           │
           ▼
      Zone N
      compute
           │
   bounded authenticated
      action protocol
           │
           ▼
      Zone S
      safety MCU
           │
           ▼
      Zone U
        target
```

Third-party snap modules remain Zone U even though they are physically inside the device stack.

## Important consequence

A physically attached module is **not** automatically trusted merely because it uses the Relmote connector.

The module descriptor is data from an untrusted peripheral.

## Owner trust

The owner should be able to:

- replace firmware;
- inspect protocol;
- recover hardware;
- manage keys.

Owner control and security are not opposites.
