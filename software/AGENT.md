# Relmote Agent

Relmote Agent is the installed or ephemeral software-node form of Relmote.

## Goals

- rich native target observations;
- no special hardware requirement;
- same identity/capability/task model as physical Relmotes;
- owner-controlled permissions;
- local-first operation;
- optional remote reachability;
- removable without breaking the target.

## Deployment forms

### Installed service

Persistent `relmoted` service for personal computers, servers, homelabs, and managed lab systems.

### Portable / ephemeral process

Run manually and exit when the support session ends.

### Temporary helper from physical Relmote

With explicit permission, Pocket may establish a richer native path to a temporary helper. The helper should not silently persist after the session.

## Candidate capabilities

Platform-specific plugins may expose:

```text
system.identify
shell.read
shell.write
file.read
file.write
network.inspect
network.configure
process.inspect
logs.read
power.read
```

Capabilities remain narrow and explicit.

## Native preference

If Agent offers an authorized native shell, Relmote should normally prefer it over emulating keyboard input.

## Security

Installed Agent does not receive blanket authority merely by existing. Controller identity, session grants, expiry, and target policy remain applicable.

## No mandatory cloud

Agent should support local LAN, USB networking, loopback/local controller, and owner VPN operation without requiring a Dev11 account or relay.
