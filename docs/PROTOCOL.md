# Relmote protocol sketch

The Relmote protocol represents intent above individual transports.

The same logical message should be serializable over:

- a local high-bandwidth connection;
- BLE;
- an IP network;
- a constrained mesh;
- store-and-forward transport.

## Core objects

### Session

Identifies:

- Relmote node;
- controller;
- target;
- mode;
- active capability grant;
- creation and expiry time.

### Capability

A named permission such as:

```text
observe.console
input.keyboard
input.pointer
shell.read
shell.write
network.inspect
power.read
power.control
storage.read
storage.write
firmware.write
```

Names are intentionally more precise than “admin.”

### Task

A durable intent.

Example:

```json
{
  "type": "task",
  "id": "task-482",
  "intent": "diagnose_network",
  "target": "home-server",
  "constraints": {
    "read_only": true,
    "expires_at": "..."
  }
}
```

### Proposal

A structured action or action group produced by a planner.

### Approval

Authorizes one proposal or a bounded class of actions.

### Result

Contains:

- status;
- structured findings;
- evidence references;
- side effects;
- errors;
- requests for additional authority.

### Event

Reports transport changes, pairing, target changes, revocation, timeout, or physical stop.

## Message properties

Messages should support:

- unique IDs;
- replay protection;
- idempotency where possible;
- acknowledgement;
- priority;
- expiry;
- chunking;
- optional compression;
- optional signatures;
- resumability.

## Low-bandwidth representation

The logical protocol should have a compact binary representation in addition to human-readable JSON.

A constrained link should favor semantic data:

```text
result: dhcp_failed
attempts: 3
link: up
need: network_config.read
```

rather than shipping megabytes of terminal output.

## Transport adapters

Transports should not interpret task semantics.

They carry protocol messages and expose capabilities; policy and routing remain above them.

## Versioning

Protocol evolution should be capability-negotiated. Unknown optional fields should be ignorable; unknown required capabilities should fail closed.
