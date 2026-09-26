# v0.1 bench bill of materials

This is a **prototype BOM**, not a final product BOM.

## Core

- Raspberry Pi Zero 2 W
- microSD card suitable for Raspberry Pi OS
- 5 V power supply/cable for the Pi's power input
- USB **data-capable** cable from the Pi's OTG/data port to the target computer

## Controls

- 1 × momentary pushbutton — **AUTHORIZE**
- 1 × momentary pushbutton — **STOP**
- 1 × LED — **ARMED**
- 1 × LED — **ACTIVITY**
- 2 × 220–470 Ω LED current-limiting resistors
- breadboard or small prototyping board
- jumper wire

The initial wiring uses GPIO internal pull-ups for buttons, so no external button resistors are required for the bench build.

## Optional but useful

- small enclosure or project box
- USB data/power breakout or short extension for strain relief
- additional LED for fault/STOP-latched state
- label tape for AUTHORIZE / STOP / TARGET / POWER

## Deliberately not required yet

- custom PCB
- battery
- LoRa radio
- Ethernet
- cellular modem
- screen
- KVM capture
- secure element
- ESP32-S3 safety MCU

Those should be added only after the first target-output safety loop is physically validated.
