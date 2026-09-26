# Remote access modes

These are user-facing policy presets, not separate protocols.

## Local only

```text
Internet rendezvous: off
public relay: off
LAN: optional
BLE/USB: on
```

Good for users who want no remote reachability.

## Ask every time

A paired controller may request a session.

A local user must approve the session/capabilities.

## One-time support

Temporary invitation.

Relationship expires after:

- one session;
- invitation expiry;
- explicit revoke.

## Trusted support

Known controller may request sessions.

The owner predefines:

- capabilities it may request;
- capabilities that always prompt;
- capabilities never allowed.

## Unattended

Specific controller/capability combinations may operate without a local approval prompt.

This must be explicitly configured.

Physical Pocket output may still require physical authorization depending on target transport/policy.

## Infrastructure

For owner-administered servers/appliances.

May use longer-lived grants and headless operation, but remains identity/capability scoped.

## Privacy transport

Prefer:

- self-hosted infrastructure;
- Tor;
- direct connections;
- owner VPN;

according to user policy.

## Custom

Advanced users define allowed connectivity adapters and priorities directly.
