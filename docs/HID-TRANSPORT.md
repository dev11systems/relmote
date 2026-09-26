# USB HID transport

Relmote's first physical target transport is deliberately narrow.

## Supported action

```text
type_text
capability: input.keyboard
payload: {"text": "..."}
```

The Linux transport does **not** accept arbitrary HID reports, keycodes, macros, mouse input, or hidden scripts.

## Why text first?

Text is enough to validate the complete physical authorization loop without prematurely exposing a general-purpose injection interface.

Before opening `/dev/hidg0`, Relmote:

1. checks the action kind;
2. requires exactly `input.keyboard`;
3. verifies that `text` is a string;
4. enforces a bounded length;
5. validates every character.

This means an unsupported character cannot cause a valid prefix to be typed before failure.

## Current keyboard model

The prototype encoder targets a standard **US USB HID keyboard layout** and supports:

- A-Z / a-z
- digits
- common ASCII punctuation
- space
- Tab
- Enter/newline

International layouts and arbitrary key combinations are intentionally deferred.

## STOP behavior

The transport accepts a synchronous `stop_requested()` predicate and checks it before each character.

When STOP becomes active:

- no new keypress is emitted;
- one all-keys-released report is emitted to avoid a stuck key;
- the action returns as interrupted;
- the action ID remains consumed rather than being replayed automatically.

The physical GPIO STOP implementation is the next hardware-facing layer.

## Prototype USB gadget

`hardware/v0.1-pi-zero/setup-hid-gadget.sh` creates a standard keyboard gadget when run on a compatible Linux SBC already configured for USB peripheral mode.

The USB vendor/product identifiers in that script are for local prototyping only and are **not a production USB identity**.

## Security boundary

Policy remains above the transport, but the transport performs its own narrow validation as defense in depth.

A future safety-MCU architecture should enforce the equivalent constraints below the Linux/AI compute plane.
