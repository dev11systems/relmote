# KVM module

**Likely class:** L or high-speed S

## Purpose

Give Relmote eyes and richer pre-OS control.

Potential functions:

- HDMI input;
- video capture;
- USB HID path;
- optional HDMI passthrough;
- optional hardware scaling/compression.

## Capabilities

```text
observe.screen
input.keyboard
input.pointer
kvm.video
```

## Why module?

KVM adds:

- high-speed signaling;
- heat;
- significant continuous power;
- bulky connectors;
- capture hardware.

It is too expensive in volume/energy to force into every Pocket.

## All-in-One

KVM is a strong candidate for native All-in-One integration.

## Evidence

Raw frames are observations.

OCR/vision/model interpretation is a separate software layer and must not replace frame provenance.
