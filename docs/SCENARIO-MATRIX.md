# Scenario matrix

This matrix maps representative use cases to reusable Relmote building blocks.

Legend:

- **B** — base Pocket
- **M** — snap/external module
- **S** — software/plugin
- **A** — likely native in All-in-One
- **O** — optional planner/AI

| Scenario | Controller path | System path | Feedback | Extra hardware | Software | Strong demo? |
| --- | --- | --- | --- | --- | --- | --- |
| Family laptop support | B: BLE/Wi-Fi/remote | B: HID + M/A: KVM | screen | KVM | controller + planner O | **Yes** |
| Broken boot/UEFI | B | B: HID + M/A: KVM | screen | KVM | controller | **Yes** |
| Router/switch recovery | B or M: mesh | M/A: serial | text | serial | console | **Yes** |
| Homelab server | B: LAN/remote | S: SSH/Redfish + M/A: KVM | text/structured/screen | optional KVM | SSH/Redfish | **Yes** |
| Headless Linux rescue | B | serial/SSH/USB network | text | maybe serial | shell | Yes |
| Remote field site | M: cellular/mesh | serial/SSH | text | cellular/mesh/serial | store-forward | **Yes** |
| Embedded bench | B | M: UART/SWD/JTAG | text/structured | debug | debug plugins | Yes |
| QA black-box test | LAN/USB | HID/KVM/serial | screen/text | KVM | task runner | Yes |
| Accessibility bridge | BLE | HID | none/optional screen | none | custom controller | Yes |
| Retrocomputing | B | legacy adapter | varies | community module | driver | Niche |
| Community network | mesh/LAN | serial/SSH | text | mesh/serial | store-forward | Yes |
| Human-only console | B | any | any | as needed | no AI | **Yes** |

## First demonstration ladder

The project should demonstrate increasing architectural depth rather than trying to build everything at once.

### Demo 0 — software safety

Already largely implemented:

```text
proposal
→ policy
→ approval
→ safety gate
→ dry-run/HID model
```

### Demo 1 — Pocket ancestor

```text
phone/laptop
→ local controller
→ Pi prototype
→ USB HID
→ sacrificial computer
```

Proves:

- physical authorization;
- STOP;
- real target output;
- no target software.

### Demo 2 — feedback

```text
controller
→ Relmote
→ USB serial / SSH
→ target
← text observation
```

Proves:

- action vs observation;
- evidence;
- bidirectional task loop.

### Demo 3 — route upgrade

Start:

```text
HID only
feedback: none
```

Then make SSH available.

Relmote moves the same task to:

```text
SSH
feedback: text
```

Proves transport-independent task semantics.

### Demo 4 — KVM support

```text
tablet
→ Relmote
→ HID + video capture
→ boot/recovery screen
```

Proves pre-OS IT support.

### Demo 5 — serial field support

```text
phone
→ BLE
→ Relmote
→ serial module
→ router
```

Proves module architecture and network-equipment support.

### Demo 6 — constrained/store-forward

```text
controller
→ mesh
→ Relmote
→ serial
→ target
```

Send compact task; return semantic result.

Proves the broader Uniline/Unilink-adjacent architecture.

## Most legible public demos

If explaining Relmote to someone new, these likely communicate it fastest:

1. **Laptop recovery with no installed agent**
2. **Router console from a phone**
3. **Same task automatically upgrades from blind HID to SSH**
4. **Remote low-bandwidth diagnostic task over mesh**
5. **Manual mode with AI completely disabled**

Together they demonstrate that Relmote is neither merely a Rubber Ducky nor merely a remote-desktop appliance.
