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
5. validates every character;
6. verifies that the physical output gate is currently armed;
7. verifies that the execution context has not been cancelled.

This means an unsupported character cannot cause a valid prefix to be typed before failure, and a disarmed target never gets opened for output.

## Current keyboard model

The prototype encoder targets a standard **US USB HID keyboard layout** and supports:

- A-Z / a-z
- digits
- common ASCII punctuation
- space
- Tab
- Enter/newline

International layouts and arbitrary key combinations are intentionally deferred.

## Two stop paths

The transport continuously observes two independent conditions.

### Session cancellation

The controller supplies a live `ExecutionContext`.

`context.should_stop()` becomes true when the active session is revoked or expires.

### Physical safety gate

The HID transport also requires an `OutputGate`.

The current `SafetyGate`:

- starts disarmed;
- arms only for a finite lease;
- automatically disarms on lease expiry;
- supports a latched STOP;
- cannot be re-armed while STOP remains latched.

For output to continue, **both** the session and physical gate must remain valid.

## Interruption behavior

When either stop path becomes active:

- no new keypress is emitted;
- one all-keys-released report is emitted if the device is already open, avoiding a stuck modifier/key;
- the action reports which path stopped it;
- the action ID remains consumed rather than being replayed automatically.

The transport checks between characters. Measuring real-world stop latency is part of the v0.1 bench validation.

## Prototype USB gadget

`hardware/v0.1-pi-zero/setup-hid-gadget.sh` creates a standard keyboard gadget when run on a compatible Linux SBC already configured for USB peripheral mode.

The USB vendor/product identifiers in that script are for local prototyping only and are **not a production USB identity**.

## Security boundary

Policy remains above the transport, while the transport performs narrow action validation as defense in depth and requires an independent output gate.

The Pi-only prototype still shares one Linux system. A later safety-MCU architecture should enforce the output gate and target-facing protocol below the Linux/AI compute plane.
