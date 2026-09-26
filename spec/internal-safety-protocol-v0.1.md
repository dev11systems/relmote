# Relmote Internal Safety Protocol v0.1 — Draft

**Status:** software-model draft. Cryptographic construction and wire encoding are not frozen.

This protocol sits between the network-facing node/compute plane and the minimal target-facing safety plane.

## Principle

The safety MCU receives **bounded actions**, never prompts.

```text
BAD:
"Fix the computer"

GOOD:
TYPE_TEXT
action_id: ...
session_id: ...
lease_id: ...
text: "hello"
```

## Threat model

Assume the compute plane may:

- crash;
- send malformed messages;
- repeat old messages;
- be compromised;
- lose connectivity;
- reboot mid-action.

The safety plane should remain fail-closed.

## Message envelope

Logical fields:

```yaml
protocol_version: 1
message_id: ...
session_id: ...
lease_id: ...
sequence: 42
command: TYPE_TEXT
payload: ...
auth: ...
```

## Commands

Initial command vocabulary:

### HELLO

Negotiate protocol/capabilities.

### QUERY_STATE

Read safety state.

### BEGIN_SESSION

Associate a controller-side session identity with a bounded safety session.

### ARM_LEASE

Request a short target-output lease.

A physical AUTHORIZE event remains required by policy/hardware.

### TYPE_TEXT

Structured text only.

The safety MCU performs its own:

- length limit;
- character validation;
- lease check;
- sequence/replay check;
- STOP check.

### RELEASE_ALL_KEYS

Explicitly emit key-up state.

### DISARM

End output authorization immediately.

### END_SESSION

Destroy safety-side session state.

## Physical events

The safety MCU emits events such as:

```text
AUTHORIZE_PRESSED
STOP_LATCHED
STOP_RESET
LEASE_EXPIRED
TARGET_ATTACHED
TARGET_DETACHED
WATCHDOG_TIMEOUT
FAULT
```

The compute plane does not synthesize physical-button events.

## Replay

Each safety session maintains a monotonic sequence or equivalent replay window.

Previously accepted target-changing messages must not be accepted again after:

- retransmission;
- reconnect;
- compute reboot.

Exact persistence strategy remains open.

## Authentication

The internal link should eventually provide message integrity/authentication so another internal device/module cannot impersonate the compute plane.

Do not invent a custom cryptographic primitive.

Candidate approach:

- device-local keys established during manufacturing/owner setup;
- standard AEAD/MAC construction;
- boot/session nonces;
- monotonic/replay state.

The exact construction requires security review before hardware freeze.

## Fail-closed behavior

Safety output disarms on:

- STOP;
- lease expiry;
- heartbeat timeout where required;
- invalid authentication;
- invalid sequence;
- malformed target-changing message;
- safety MCU reset;
- undefined command.

## Transport independence

The logical protocol should run over:

- UART for early prototypes;
- USB;
- SPI;
- another future internal transport.

Wire framing belongs below message semantics.
