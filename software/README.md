# Relmote software

Relmote software is a **headless core plus interchangeable controllers**.

The product is not one phone app.

```text
 iOS/iPadOS     Android/GrapheneOS     Web/PWA      CLI/TUI
      \               |                 |            /
       \              |                 |           /
        └──────── Relmote Controller Protocol ──────┘
                           │
                    ┌──────▼──────┐
                    │ relmoted    │
                    │ node daemon │
                    └──────┬──────┘
                           │
              policy / sessions / routing
                           │
               ┌───────────┼────────────┐
               │           │            │
           transports    modules     planners
               │                        │
             target              human / local AI /
                                  phone / server /
                                      cloud
```

See also:

- [Software-first MVP](SOFTWARE-MVP.md)
- [Node implementations](NODE-IMPLEMENTATIONS.md)
- [Relmote Agent](AGENT.md)
- [Relmote Live](LIVE.md)
- [Daemon](DAEMON.md)
- [Controller UX](CONTROLLER-UX.md)
- [Client forms](CLIENTS.md)
- [Discovery](DISCOVERY.md)
- [Remote access](REMOTE-ACCESS.md)
- [Pairing UX](PAIRING-UX.md)
- [Access modes](ACCESS-MODES.md)
- [Planner architecture](PLANNERS.md)
- [Task lifecycle](TASK-LIFECYCLE.md)
- [Observations/evidence](OBSERVATIONS.md)
- [Store-and-forward](STORE-AND-FORWARD.md)
- [Constrained links](CONSTRAINED-LINKS.md)
- [Controller API draft](../spec/controller-api-v0.1.md)

## Components

### `relmoted`

The node daemon.

Responsibilities:

- node identity;
- controller pairing;
- session lifecycle;
- capability discovery;
- module discovery;
- policy;
- transport routing;
- task/proposal/result state;
- audit metadata;
- store-and-forward;
- local API.

It should remain useful with **no AI configured**.

### Companion clients

Different front ends should expose the same underlying concepts:

- node;
- target;
- path;
- mode;
- capabilities;
- task;
- proposal;
- approval;
- result;
- STOP/revoke.

### Planner adapters

A planner proposes actions.

Possible planners:

- human;
- deterministic script;
- local model;
- phone-hosted model;
- home-server model;
- cloud model.

A planner never receives direct transport authority.

### Transport plugins

Transport adapters expose capabilities and perform already-authorized operations.

Examples:

- USB HID;
- USB serial;
- Bluetooth HID;
- SSH;
- KVM;
- Redfish;
- MeshCore.

### Module drivers

Module drivers translate discovered hardware into capabilities/transports.

A module descriptor is not itself trusted authority.

## Offline-first

Local ownership must work without:

- Dev11 account;
- Dev11 cloud;
- Internet;
- AI provider.

Remote/cloud features are additive.

## API principle

Controller APIs should expose **semantic objects**, not internal Python classes or raw hardware handles.

This keeps clients portable and lets the daemon evolve independently.
