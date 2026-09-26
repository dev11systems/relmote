# Relmote Mini — reference concept

**Goal:** the smallest useful Relmote-compatible hardware.

Mini proves that Relmote is a protocol/platform rather than a premium Linux appliance.

## Possible implementation

A small MCU-class board with:

- native USB;
- BLE and/or Wi-Fi;
- minimal status indication;
- physical authorize/stop;
- optional small battery.

## Typical capabilities

```text
controller:
  BLE
  Wi-Fi (optional)

system:
  USB HID
  USB serial
  Bluetooth HID (optional)
```

No local large model is required.

A phone, laptop, home server, or cloud planner may provide intelligence.

## Uses

- inexpensive DIY build;
- dedicated HID/serial node;
- embedded appliance;
- safety plane for a larger Relmote;
- remote module endpoint.

## Philosophy

A $15–30 experimental board should be able to implement meaningful Relmote semantics.

The ecosystem should not require expensive hardware to participate.
