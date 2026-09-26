# Relmote Controller API v0.1 — Draft

**Status:** semantic API draft; wire protocol not frozen.

The controller API connects companion clients to `relmoted`.

## Resources

### Node

```json
{
  "node_id": "rm:example",
  "name": "pocket-01",
  "state": "online",
  "controller_paths": ["ble", "wifi"],
  "power": {"battery_percent": 74}
}
```

### Target

```json
{
  "target_id": "target:example",
  "name": "ThinkPad",
  "system_paths": ["usb.hid"],
  "feedback": "none"
}
```

### Session

```json
{
  "session_id": "...",
  "mode": "assist",
  "target_id": "target:example",
  "capabilities": ["input.keyboard"],
  "expires_at": "..."
}
```

### Task

Durable human intent.

### Proposal

Structured candidate action(s).

### Approval

Explicit authorization for a proposal/action or bounded capability set.

### Result

Structured outcome/evidence.

### Event

State changes such as:

- node path changed;
- target attached;
- physical authorization requested;
- physical authorization granted;
- STOP latched;
- lease expired;
- module added;
- task completed.

## Candidate endpoints

Illustrative only:

```text
GET  /v1/node
GET  /v1/targets
GET  /v1/capabilities
GET  /v1/modules
GET  /v1/sessions
POST /v1/sessions
POST /v1/sessions/{id}/revoke

POST /v1/tasks
GET  /v1/tasks/{id}

POST /v1/proposals/{id}/approve
POST /v1/proposals/{id}/reject

GET  /v1/events
WS   /v1/events
```

## Safety rule

The API can request physical authorization.

It cannot manufacture a physical authorization event.

## Authentication

Local transport does not mean unauthenticated transport.

Pairing/authentication details remain open, but controller identity must survive changes between BLE/Wi-Fi/USB.

## Constrained links

This HTTP-shaped API is **not** the LoRa wire format.

Semantic objects should have compact representations for constrained transports.

The controller API and low-bandwidth protocol share meaning, not necessarily framing.
