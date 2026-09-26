# v0.1 — Pi Zero bench prototype

Status: **planned**

## Success criterion

An authorized controller sends a text action to Relmote. Relmote:

1. identifies the target session;
2. evaluates the requested capability;
3. requires approval when appropriate;
4. emits the approved text exactly once as USB HID;
5. records metadata in the audit log;
6. immediately refuses all further output after revocation.

## Initial hardware

- Raspberry Pi Zero 2 W or equivalent USB-device-capable Linux SBC
- microSD
- USB data connection to a sacrificial test machine
- momentary authorization button
- momentary STOP button
- at least two status indicators

## Software layers

```text
RelmoteController
      │
 policy/session
      │
 LinuxHIDTransport
      │
 /dev/hidg0
      │
 USB gadget HID
      │
 target
```

## Test sequence

Start with a blank text editor on a sacrificial target.

### Test A — no authorization

Propose input and verify that no HID report is emitted.

### Test B — Assist approval

Approve one action and verify that its text appears exactly once.

### Test C — replay

Retry the same action ID and verify no additional text is emitted.

### Test D — revoke

Authorize a session, revoke it, then attempt output. Verify zero target-side input.

### Test E — expiry

Allow a short session to expire and verify output fails closed.

### Test F — physical STOP

While a permitted sequence is active, press STOP and verify target output ceases immediately.

## Not in v0.1

- autonomous terminal reasoning
- hidden background control
- privilege escalation
- persistence on the target
- KVM/video
- mesh
- custom PCB

Those belong after the physical authorization boundary is proven.
