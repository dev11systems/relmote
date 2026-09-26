# Hardware strategy

Relmote should validate the product architecture before committing to a custom PCB.

The hardware strategy therefore has two stages:

1. **single-board proof** — prove the physical interaction loop quickly;
2. **split-plane prototype** — separate the safety-critical target interface from higher-level compute.

## v0.1 bench prototype

Initial candidate: **Raspberry Pi Zero 2 W**.

Why it is useful for the first physical proof:

- runs the existing Python Relmote core directly;
- USB OTG/device support;
- Linux USB gadget stack can expose HID;
- onboard Wi-Fi and BLE;
- GPIO is available for physical authorization and stop controls;
- small enough to approximate the eventual portable form factor.

The first prototype is not the final hardware architecture.

### v0.1 topology

```text
phone / tablet / laptop
          │
      Wi-Fi / BLE
          │
   ┌──────▼──────┐
   │ Pi Zero 2 W │
   │             │
   │ Relmote     │
   │ policy      │
   │ session     │
   │ audit       │
   │ USB gadget  │
   └──────┬──────┘
          │
       USB HID
          │
      test target
```

### Required physical controls

The bench build should include:

- authorization button;
- immediate stop/revoke button;
- visible armed/operate indicator;
- visible target-output activity indicator.

The stop path must not depend on an AI model.

## v0.2 split-plane prototype

Once the loop works, move target-facing USB/input responsibility into a dedicated microcontroller.

Candidate class: **ESP32-S3** or another MCU with native USB device support.

```text
        controller
            │
       BLE / Wi-Fi
            │
    ┌───────▼────────┐
    │ compute plane  │
    │ Linux / agent  │
    │ planner/router │
    └───────┬────────┘
            │ authenticated internal protocol
    ┌───────▼────────┐
    │ safety plane   │
    │ MCU            │
    │ policy gate    │
    │ physical stop  │
    │ HID/USB        │
    └───────┬────────┘
            │
          target
```

This allows the MCU to refuse output even if the higher-level operating system, application, or AI behaves incorrectly.

## Longer-term modular hardware

Potential modules:

- Core
- Console / UART / RS-232
- Ethernet
- LoRa / mesh
- KVM/video capture
- cellular modem
- battery/power module
- external secure element
- storage/recovery media

Modules should expose capabilities to Relmote rather than forcing the agent to know board-specific details.

## Open questions

- Which functions belong permanently in the MCU safety plane?
- Should controller BLE terminate on the MCU, Linux side, or both?
- What physical control layout is understandable without reading documentation?
- Should target USB power Relmote, or should Relmote remain independently powered?
- What should happen electrically when STOP is pressed: logical revoke, USB disconnect, or both?
- Which functions should remain usable when Linux fails to boot?
