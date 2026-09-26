# Access lifecycle

Relmote separates **software availability**, **network reachability**, **controller trust**, and **active support authority**.

A user may keep Relmote installed without keeping support access active.

## Layers

```text
Relmote installed
      │
      ├─ remote listener disabled
      │
      └─ remote listener enabled
             │
       known controller
             │
       support grant/session
             │
       target capabilities
```

Each layer can be changed independently.

## User-facing states

### Installed / dormant

Relmote is installed but accepts no remote controller connection.

Useful default for personal support machines.

### Available on demand

User selects:

```text
Enable support
```

Relmote begins listening on configured private interfaces.

The user later selects:

```text
Disable support
```

No reinstall/reconfiguration is needed.

### Timed availability

User may choose:

- 15 minutes;
- 1 hour;
- 4 hours;
- until reboot;
- custom duration.

When the availability window ends, the listener returns to dormant state.

### Until manually disabled

User explicitly chooses persistent availability.

This is useful for:

- trusted family support;
- homelabs;
- servers;
- infrastructure.

It should be visibly distinct from a timed session.

## Existing private networks

If the machine already participates in Tailscale, WireGuard, or another owner-approved private network, Relmote should be able to bind only to that interface/address.

This is preferable to opening a public Internet listener.

Example:

```text
Rae controller
     │
  Tailscale
     │
cousin machine
     │
 Relmote
```

Tailscale provides reachability/encrypted networking.

Relmote still provides:

- controller identity;
- support policy;
- capabilities;
- task/evidence model;
- revoke.

## Availability versus session expiry

These are different.

Example:

```text
Relmote availability:
  until manually disabled

Rae support grant:
  read-only diagnostics
  no expiry

keyboard grant:
  ask every time
  15 minutes
```

A persistent listener does not require persistent write authority.

## Re-activation

If support is disabled:

```text
Enable support
```

should restore the configured listener/trusted-controller policy without requiring a new install.

The user may optionally require re-pairing or clear previous trust.

## Startup policy

Installed Agent may offer:

- dormant at startup;
- enable on startup on private interfaces;
- restore previous state;
- infrastructure mode.

Default for ordinary personal computers should favor dormant/on-demand access until the owner chooses otherwise.

## Interface binding

Possible policies:

- localhost only;
- selected LAN interface;
- selected Tailscale/WireGuard interface;
- all private interfaces;
- explicit addresses.

Avoid defaulting to every interface.

## Emergency revoke

The local user should always have a simple:

```text
DISABLE SUPPORT
```

control that:

- closes remote listeners;
- revokes active sessions;
- preserves installation/configuration unless they choose to remove it.

## Principle

> **Persistent installation does not imply persistent access, and persistent reachability does not imply persistent authority.**
