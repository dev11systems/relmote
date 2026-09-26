# Controller UX

A controller should answer five questions immediately:

1. **Which Relmote am I controlling?**
2. **What target is it attached to?**
3. **How am I reaching Relmote?**
4. **How is Relmote reaching the target?**
5. **What authority is currently active?**

## Home / node view

Example:

```text
╭────────────────────────────────╮
│ Relmote Pocket · rm-7A21       │
│ ● nearby · BLE                 │
│                                │
│ TARGET                         │
│ ThinkPad · USB HID             │
│ feedback: none                 │
│                                │
│ MODE                           │
│ ASSIST · read/input grant      │
│ physical gate: ARMED 00:12     │
│                                │
│ [ New task ]      [ REVOKE ]   │
╰────────────────────────────────╯
```

The UI must not imply that “connected” means “authorized.”

## Path view

Relmote should make paths visible:

```text
iPad
  ↓ BLE
Relmote Pocket
  ↓ USB HID
ThinkPad
```

For a remote node:

```text
GrapheneOS
  ↓ cellular / Internet
home gateway
  ↓ WireGuard / future Unilink
Relmote
  ↓ serial
router
```

For constrained mesh:

```text
controller
  ↓ BLE
mesh node
  ↓ LoRa / MeshCore
remote Relmote
  ↓ UART
target
```

## Task composer

A user should be able to enter:

```text
"Check whether this machine sees its NVMe drive."
```

But Relmote should show the resulting proposal before target-changing action when policy requires it.

```text
PROPOSAL

1. Type: lsblk
   capability: input.keyboard
   feedback: unavailable

⚠ Relmote cannot read the result with the current path.

[ Teach me ] [ Approve anyway ]
```

This is important: the UI should surface **epistemic limitations** such as blind HID.

## Modes

### Observe

No target-side input.

### Teach

Show the human what to do.

### Assist

Prepare actions; approval is required.

### Operate

Execute only inside an explicit bounded grant.

The active mode should remain visible throughout a session.

## Physical authorization

A controller can request authorization but cannot fake a physical AUTHORIZE press.

Example:

```text
Target input needs physical authorization.

Press AUTHORIZE on rm-7A21.

Waiting…  ○
```

## STOP

STOP/revoke should be available in software, but the physical STOP remains authoritative.

The UI should distinguish:

- software session revoked;
- physical STOP latched;
- output lease expired.

## Multiple Relmotes

Node browser:

```text
MY RELMOTES

● rm-pocket-01    nearby · BLE
  ThinkPad         USB HID

● homelab-kvm     online · LAN
  proxmox-01       KVM + SSH

○ field-node-3     last seen 18m
  queued task: 1
```

Never automatically choose among multiple target-affecting nodes solely because one has a stronger signal.

## Accessibility

- do not rely on color alone;
- large STOP/revoke target;
- readable path diagrams;
- concise default view with expandable technical detail;
- keyboard/screen-reader navigation;
- reduced-motion support;
- explicit text labels for mode and authority.
