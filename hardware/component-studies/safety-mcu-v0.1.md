# Safety MCU study v0.1

The safety MCU owns the smallest trusted target-output boundary.

## Required functions

- physical STOP;
- AUTHORIZE lease;
- watchdog;
- target-side USB HID or equivalent low-level gate;
- status indicators;
- authenticated internal command channel;
- safe boot;
- local recovery/debug;
- low-power always-on operation.

## Candidate: RP2350 class

RP2350 is currently a particularly attractive reference candidate because it offers:

- USB 1.1 host/device controller + PHY;
- dual Cortex-M33 or Hazard3 RISC-V cores;
- SWD;
- UART/SPI/I²C;
- programmable I/O;
- OTP/security features;
- open C/C++ SDK;
- published minimal KiCad reference designs;
- long stated production horizon.

### Advantages

- unusually good documentation;
- easy DIY development;
- no opaque wireless stack because wireless is not its job;
- USB target plane can remain independent of Linux;
- inexpensive enough to duplicate in prototypes/test fixtures.

### Limitations

- USB full-speed only;
- no integrated BLE/Wi-Fi;
- security architecture still needs our own careful design;
- target-side high-speed functions remain outside the MCU.

These are mostly acceptable because the safety plane should remain narrow.

## Candidate: ESP32-S3 class

Advantages:

- native USB;
- Wi-Fi/BLE;
- huge maker ecosystem;
- could combine controller BLE with safety functions in Mini.

Tradeoff:

- putting radios/network stack inside the trusted safety MCU increases its attack surface and complexity.

**Position:** excellent Mini candidate and prototype alternative; for Pocket, prefer keeping network-facing radio complexity out of the minimal safety plane unless there is a strong reason.

## Architecture preference

Pocket:

```text
Linux/node plane
      │ authenticated narrow protocol
      ▼
RP2350-class safety MCU
      │
target-facing HID / STOP / LEDs
```

Mini may collapse these roles onto one ESP32-S3-class MCU.

## Required prototype tests

- Linux process crashes while typing;
- Linux sends malformed command;
- command replay;
- STOP during output;
- watchdog timeout;
- MCU reset during output;
- USB disconnect/reconnect;
- power brownout;
- unauthorized firmware;
- recovery mode.

## Design rule

The safety MCU should understand **actions**, not AI prompts.

Example:

```text
TYPE_TEXT action-id=... length=...
```

not:

```text
"fix this computer"
```
