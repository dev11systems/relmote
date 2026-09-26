# MVP-1 bench bring-up

This checklist is for a **sacrificial test computer you own/control**.

## 1. Prepare the Pi

- Install a supported Raspberry Pi OS image.
- Update packages.
- Install Python 3.11+ tooling and Git.
- Clone the Relmote repository.
- Install the package in editable mode with test dependencies.
- Run the test suite before connecting a target.

Expected:

```text
pytest -q
→ all tests pass
```

## 2. Configure USB peripheral mode

The Pi Zero-class board must expose its OTG/data port as a USB peripheral.

Exact boot configuration varies by OS release; verify the current Raspberry Pi documentation for the installed image rather than copying an old tutorial blindly.

After peripheral mode is working, use:

```text
hardware/v0.1-pi-zero/setup-hid-gadget.sh
```

Expected device:

```text
/dev/hidg0
```

## 3. Wire controls

Follow [WIRING.md](WIRING.md).

Do **not** connect the target yet.

Verify:

- AUTHORIZE button reads correctly;
- STOP button reads correctly;
- ARMED LED follows the 15-second lease;
- ACTIVITY LED can be controlled;
- first AUTHORIZE after STOP only resets STOP;
- second AUTHORIZE arms.

## 4. Connect a sacrificial target

Use:

- a blank text editor;
- no unsaved work;
- no privileged terminal;
- no production machine.

Connect only the Pi OTG/data port to the target.

## 5. Test disarmed behavior

With the physical gate disarmed, request a text action.

Expected:

```text
characters_sent: 0
stopped_by: safety_gate
```

Target receives nothing.

## 6. Test one authorized action

Create a fresh action:

```text
hello from Relmote
```

Approve it in Assist mode.

Press AUTHORIZE.

Execute once. The MVP-1 bench harness consumes/disarms the physical lease after that dispatch, even if time remains.

Expected:

- text appears exactly once;
- activity indicator shows output;
- action ID becomes consumed.

## 7. Test replay

Attempt the exact same action ID again.

Expected:

- denied;
- no additional target input.

## 8. Test STOP

Use a deliberately long harmless text string and slower key delay.

While output is occurring:

- press STOP.

Expected:

- next target keypress is suppressed;
- release report is sent;
- output stops;
- STOP remains latched;
- action ID remains consumed.

Record observed stop latency.

## 9. Test STOP reset semantics

Press AUTHORIZE once.

Expected:

- STOP clears;
- device remains disarmed.

Press AUTHORIZE again.

Expected:

- fresh 15-second lease.

## 10. Test expiry

Arm and wait >15 seconds.

Attempt a fresh action.

Expected:

- zero output.

## 11. Test unsupported character

Request text containing an unsupported character.

Expected:

- validation fails before opening the target HID device;
- zero prefix characters appear.

## 12. Record results

Create a dated note under:

```text
hardware/v0.1-pi-zero/results/
```

Include:

- Pi model;
- OS version;
- target OS;
- cable;
- test results;
- stop latency;
- failures;
- photos/logic traces if useful.

Do not mark MVP-1 complete until the physical STOP behavior is measured on real hardware.
