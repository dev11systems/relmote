# Transport model

Relmote treats transports as interchangeable adapters behind a common capability model.

## Controller transports

These connect a human, companion application, or upstream agent to Relmote.

Candidate transports include:

- BLE GATT
- Wi-Fi LAN
- Relmote-hosted Wi-Fi access point
- Ethernet
- USB device/network connection
- Internet via an upstream network
- cellular via an attached modem or companion
- LoRa
- Meshtastic
- MeshCore
- future Uniline / Unilink paths
- future store-and-forward gateways

Controller transports may be high-bandwidth and interactive or extremely constrained and intermittent.

## System transports

These connect Relmote to the target computing system.

### Input-only / low-feedback

- USB HID keyboard
- USB HID mouse
- Bluetooth HID

These are valuable fallbacks but should be treated as **blind** unless another feedback channel exists.

### Bidirectional text

- USB CDC ACM serial
- Bluetooth RFCOMM/SPP where appropriate
- BLE GATT text service
- TTL UART
- RS-232
- device console ports

### Network-native

- USB Ethernet gadget
- Ethernet
- Wi-Fi
- SSH
- HTTPS / device APIs
- PowerShell remoting or other platform-specific management interfaces

### Visual / out-of-band

- HDMI/DisplayPort capture + USB HID KVM
- Redfish/BMC
- Intel AMT or similar out-of-band management where already configured and authorized

## Composite paths

Input and feedback do not need to use the same transport.

Examples:

```text
input:     USB HID
feedback:  HDMI capture
control:   BLE from phone
```

```text
input/output: SSH
control:      local Wi-Fi
planner:      phone
```

```text
input/output: UART
control:      LoRa mesh
planner:      remote server
```

## Transport capabilities

Every transport adapter should report structured metadata such as:

```text
direction: input | output | bidirectional
media: text | events | screen | file | structured-api
interactive: true/false
bandwidth
latency
reliability
metered/cost
power-cost
requires-target-helper
works-before-os
supports-authentication
supports-encryption
```

The router uses this metadata along with task requirements and current authorization.

## Constrained transports

LoRa and mesh links should not be treated as slow TCP replacements.

Relmote should support:

- compact task messages;
- structured status;
- resumable chunks;
- acknowledgements;
- priority;
- expiry;
- idempotency;
- store-and-forward;
- semantic summaries instead of raw bulk logs.

Example:

```text
TASK: diagnose-network
MODE: read-only

RESULT:
link=up
dhcp=failed
gateway=unknown

EVIDENCE:
dhcp timeout x3

REQUEST:
read NetworkManager configuration?
```

## Transport selection

The router should prefer the least-invasive transport that satisfies the task.

Examples:

- use an authorized SSH session for shell work instead of HID;
- use Redfish for server power state instead of visually navigating a BMC UI;
- use serial when the OS network stack is unavailable;
- use KVM/HID when no cooperative software path exists;
- use HID alone only when sufficient for the task or no richer feedback path exists.
