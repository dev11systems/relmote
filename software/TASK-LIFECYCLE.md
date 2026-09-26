# Task lifecycle

A Relmote **task** represents durable intent above transports.

The task should survive:

- controller path changes;
- system path changes;
- temporary disconnection;
- daemon restart where persistence permits;
- constrained links;
- planner changes.

## States

```text
CREATED
   │
   ▼
PLANNING
   │
   ▼
WAITING_APPROVAL ─────► REJECTED
   │
   ▼
WAITING_CAPABILITY
   │
   ▼
READY
   │
   ▼
RUNNING
   │
   ├────► WAITING_OBSERVATION
   │             │
   │             └────► RUNNING
   │
   ├────► PAUSED
   │
   ├────► FAILED
   │
   └────► COMPLETED
```

Not every task visits every state.

## Durable intent

Example:

```text
Diagnose why networking is unavailable.
Constraints:
- read only
- target: router-01
- expires in 6h
- do not reboot
```

The task does not say:

```text
send these exact 184 UART bytes
```

That belongs below the task layer.

## Route changes

Suppose a task begins with:

```text
controller → BLE → Relmote
Relmote → USB HID → target
```

Later the target exposes an authorized SSH path.

Relmote may re-plan remaining work through SSH if:

- task semantics remain equivalent;
- current grant permits it;
- the new path is authenticated appropriately;
- no partially emitted action is replayed.

Route changes generate events and remain visible to the controller.

## Lost controller

Interactive tasks normally pause when required approvals cannot be obtained.

Store-and-forward tasks may continue only when the original grant explicitly permits autonomous continuation.

## Expiry

A task may have:

- task expiry;
- session expiry;
- physical output lease expiry.

These are separate.

An unexpired task does not keep an expired authorization alive.

## Cancellation

Cancellation stops future task work.

It does not pretend to undo already completed side effects.

## Idempotency

Actions that may have partially executed are never automatically replayed merely because an acknowledgement was lost.

A planner must reason from fresh observation or request a new explicit action.
