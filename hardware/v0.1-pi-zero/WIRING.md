# v0.1 Pi Zero wiring

This is the proposed bench pinout. It intentionally avoids pins commonly reserved for basic I²C/SPI experiments so later prototype expansion remains easy.

## GPIO assignment

| Function | BCM GPIO | Physical header pin | Wiring |
| --- | ---: | ---: | --- |
| AUTHORIZE button | GPIO17 | 11 | button between GPIO17 and GND |
| STOP button | GPIO27 | 13 | button between GPIO27 and GND |
| ARMED LED | GPIO22 | 15 | GPIO22 → resistor → LED → GND |
| ACTIVITY LED | GPIO23 | 16 | GPIO23 → resistor → LED → GND |
| Ground | — | 14 or another GND | shared control ground |

Buttons are intended to use software-configured internal pull-ups and therefore read active-low.

**Pi GPIO is 3.3 V logic. Do not place 5 V on GPIO pins.**

## USB layout

```text
5 V power
   │
   ▼
Pi Zero 2 W
   │
   ├── Wi-Fi / BLE  ← controller
   │
   └── USB OTG/data ─────► authorized test computer
```

Use the Pi's power input for power and the OTG/data-capable USB port for the target connection.

## Proposed control semantics

### AUTHORIZE

A press grants a short physical output lease, initially **15 seconds**.

The lease:

- does not bypass Relmote session policy;
- does not approve an otherwise unapproved Assist action;
- only permits the already-authorized target transport to emit output;
- expires automatically.

### STOP

STOP:

1. immediately disarms output;
2. latches the physical safety gate;
3. interrupts an in-progress HID action at the next transport cancellation check;
4. prevents re-arming until physically reset.

For the first bench prototype, pressing AUTHORIZE while STOP is latched should **clear STOP but remain disarmed**. A second AUTHORIZE press is then required to arm.

That prevents one accidental press from both clearing an emergency stop and re-enabling output.

## Indicators

### ARMED

On only while the physical output lease is valid.

### ACTIVITY

On/blinking only while target-side output is actually being emitted.

A later revision should add a distinct STOP/fault indication rather than overloading ARMED.

## Safety boundary

The v0.1 button logic may still run in the Linux prototype process. This validates interaction and semantics, but it is **not** the final hardware safety boundary.

The planned split-plane revision moves target-facing output and physical STOP enforcement onto a dedicated MCU so Linux/AI failure cannot override the interlock.
