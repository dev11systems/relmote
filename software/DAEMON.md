# relmoted

`relmoted` is the headless node service.

The current Python package contains the first framework-neutral pieces; there is not yet a production daemon process.

## Internal layers

```text
controller adapters
  BLE / HTTP / WebSocket / USB / mesh
               │
               ▼
        semantic API
               │
       node / target state
               │
       task + route selection
               │
      session / policy engine
               │
         transport plugins
               │
             target
```

Separate side channels:

```text
module discovery ──► capabilities
power manager    ──► budgets
event stream     ──► every controller
planner adapters ──► proposals only
```

## Storage

Persistent storage will eventually need:

- node identity;
- paired controllers;
- target aliases;
- sessions/grants;
- tasks;
- proposals/results;
- audit metadata;
- event checkpoints;
- module history;
- owner settings.

Do not use persistent storage as the source of physical authorization state.

## Local API

The Python `LocalControllerAPI` is intentionally transport/framework-neutral.

Future adapters may expose it through:

- HTTPS + WebSocket;
- BLE GATT;
- local Unix socket;
- USB network;
- constrained protocol.

## Event model

Controllers should subscribe to semantic events instead of polling raw hardware.

Examples:

```text
target.attached
path.changed
module.attached
physical.authorize_pressed
physical.stop_latched
lease.expired
task.result
```

## Concurrency

The daemon will eventually need asynchronous task handling.

Safety-critical output cancellation must not depend on a congested UI/event loop; the safety MCU remains the final boundary.

## Failure model

If `relmoted` crashes:

- safety output should disarm;
- clients reconnect;
- durable tasks recover conservatively;
- partially dispatched actions are not replayed automatically.
