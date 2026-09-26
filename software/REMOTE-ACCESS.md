# Remote access

Relmote remote access separates four concepts:

1. **identity** — which controller and node are these?
2. **reachability** — how can packets/messages get between them?
3. **authentication** — did the paired identities establish the session?
4. **authorization** — what may this controller do to this target right now?

No connectivity mechanism should collapse these into one concept.

## Default architecture

A future easy/default remote path should aim for:

```text
controller
    │
    ├── discover/rendezvous
    │
    ▼
attempt direct encrypted P2P
    │
    ├── success ───────────────► node
    │
    └── blocked
          │
          ▼
     encrypted relay
          │
          ▼
         node
```

The relay is a reachability service, not the authority over the Relmote session.

## Outbound-first node

Relmote Agent should not require an inbound firewall port for the normal remote-support workflow.

The node may maintain an outbound rendezvous/control path and accept an authenticated controller through:

- direct peer-to-peer path when available;
- encrypted relay when direct connection fails.

## Connectivity adapters

Relmote should be able to use:

- LAN;
- direct IPv4/IPv6;
- user-managed port forwarding if deliberately configured;
- native Relmote P2P/rendezvous;
- native or self-hosted Relmote relay;
- WireGuard;
- Tailscale;
- other mesh VPNs;
- Tor onion service;
- outbound reverse-tunnel providers;
- BLE;
- USB;
- constrained mesh/radio;
- custom third-party adapters.

A node may advertise multiple candidates.

## Candidate selection

A controller should prefer according to owner policy and path properties, not one hard-coded global ordering.

Possible preference:

```text
local direct
direct authenticated P2P
owner VPN
self-hosted relay
configured public relay
privacy transport
constrained/store-forward
```

Users may override this.

## Relmote rendezvous

A rendezvous service may help paired identities exchange connection candidates.

It should not receive:

- target capabilities beyond what routing strictly needs;
- task plaintext;
- shell data;
- screen data;
- session authorization secrets.

## Relmote relay

A relay forwards encrypted Relmote traffic when direct connectivity is impossible.

Desired properties:

- end-to-end encryption between controller and node;
- relay cannot decrypt session contents;
- relay replaceable without re-pairing identities;
- multiple relay operators;
- self-hostable;
- no relay-specific authorization semantics.

## Self-hosting

A user should be able to run:

```text
relmote-rendezvous
relmote-relay
```

on:

- VPS;
- home server;
- community infrastructure;
- organization infrastructure.

A Dev11-hosted service may be convenient but must not be required for protocol ownership.

## LAN-only mode

A node may be configured:

```text
remote access: disabled
LAN: allowed
BLE/USB: allowed
```

No background public rendezvous is required.

## Direct-only mode

Advanced users may choose:

```text
direct paths only
no public relay
```

Failure to establish direct reachability should remain visible rather than silently weakening policy.

## Tor

A Tor/onion adapter can provide a privacy-oriented remote path without requiring a public inbound address.

Tor reachability remains a transport property; Relmote controller/node authentication still applies.

## Existing VPNs

If a user already has Tailscale/WireGuard/etc., Relmote should simply discover/use that IP path.

Do not require users to replace functioning private networking.

## One-time support

A node may create a temporary support invitation.

The invitation can identify:

- node identity;
- rendezvous candidates;
- invitation expiry;
- maximum requestable capability envelope;
- one-time pairing material.

It does **not** silently grant all capabilities.

After expiry/session completion, the temporary controller relationship can disappear.

## Trusted support

A paired controller may be allowed to request future sessions without repeating full pairing.

Target capabilities remain separately configurable:

```text
may request:
  system.identify
  network.inspect
  logs.read

always ask:
  input.keyboard
  shell.write

never:
  privilege.elevate
```

## Unattended access

Unattended access is an explicit configuration, not an installation side effect.

It must specify:

- controller identity;
- target scope;
- capabilities;
- expiry/renewal policy where applicable;
- whether planner automation is allowed.

## Browser controller

A browser/PWA may connect through the same remote-access layer.

The browser should not require the node to expose an unauthenticated public web UI.

## Path changes

A remote session may migrate:

```text
LAN → Wi-Fi Internet → relay → direct IPv6
```

without changing:

- node identity;
- task identity;
- target identity;
- active authorization.

The path-change event remains visible.

## Metadata

Even a blind relay may observe metadata such as:

- endpoint network addresses;
- timing;
- byte counts;
- relay account/node routing identifier.

Relmote documentation should describe this honestly rather than calling relay operation “zero knowledge” without qualification.

## Security rule

> **Reachability never grants capability.**

A controller that can reach a Relmote node but lacks a valid paired identity/session grant can do nothing target-affecting.
