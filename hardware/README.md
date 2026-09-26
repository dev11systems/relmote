# Hardware

This directory tracks Relmote prototype hardware.

## Planned stages

### `v0.1-pi-zero/`

Single-board bench proof:

```text
controller → Wi-Fi/BLE → Relmote → USB HID → test target
```

Goals:

- prove real HID output;
- prove exact-action approval;
- prove immediate revocation;
- prove visible activity;
- measure latency and reliability.

### `v0.2-safety-mcu/`

Split compute and safety planes.

Goals:

- MCU owns target-facing HID;
- authenticated internal command protocol;
- physical STOP enforced below the agent;
- watchdog/fail-closed behavior;
- later composite USB functions.

No custom PCB should be designed until these stages expose the actual requirements.
