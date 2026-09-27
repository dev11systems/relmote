# Tailscale integration

Tailscale is an optional **private reachability adapter** for Relmote.

It does not replace Relmote identity, pairing, session policy, capability grants, revocation, or evidence. Tailscale answers whether two devices may reach each other over an encrypted private network; Relmote answers what an authenticated controller or Agent session may do.

## Preferred preview pattern: direct Tailscale binding

For the current Agent Access preview, Relmote prefers a direct listener bound to the target's detected Tailscale IPv4 address.

Conceptually:

```text
Agent Host
    │
    │ encrypted Tailscale/WireGuard path
    ▼
100.x.y.z:8788
Relmote Agent API
    │
    ▼
scoped pairing + capability grants
```

When Agent Access is OFF, the remotely reachable Agent listener is not started.

When Agent Access is enabled, Relmote:

1. detects the target's local Tailscale IPv4 address;
2. binds the Agent API only to that exact address and port;
3. does not bind the Agent API to `0.0.0.0`;
4. continues to require one-time pairing for credential exchange;
5. requires the scoped Agent bearer for subsequent operations.

This path does not require Tailscale Serve, HTTPS certificate setup, or administrative access to the tailnet that owns the target. That makes it suitable for ordinary nodes and for machines shared into another tailnet when Tailscale ACLs permit inbound access.

The direct endpoint currently uses HTTP at the application layer because Tailscale encrypts the network path. Relmote authorization remains mandatory on top of that encrypted transport.

## Human Controller web interface

The browser Controller may also bind directly to the detected Tailscale address when Relmote's automatic private-network exposure selects Tailscale.

Controller authentication and Agent authentication are separate. A Controller token is not an Agent bearer credential.

## Tailscale Serve is optional

Tailscale Serve can add useful HTTPS convenience, but enabling Tailscale HTTPS has a privacy side effect that Relmote must not hide: public-CA TLS certificates are recorded in Certificate Transparency logs, including the device's fully qualified `*.ts.net` name. Tailscale requires an acknowledgment before enabling HTTPS and warns against sensitive machine names.

Relmote must therefore never auto-enable Tailscale HTTPS, auto-accept that consent, or treat refusal as a failure when direct private reachability is available.

Tailscale Serve can still be useful as an optional HTTPS convenience layer:

```text
Agent Host
    │
    ▼
https://node.example.ts.net
    │
Tailscale Serve
    │
    ▼
loopback Relmote service
```

However, Serve can require tailnet-level feature enablement, HTTPS certificate setup, or administrative rights that the local target operator may not possess. Relmote therefore must not make Serve a prerequisite for Agent Access.

Relmote should surface Serve as an optional transport/provider when it is already configured or deliberately selected.

## Why exact-interface binding matters

Relmote should never turn "private reachability requested" into "listen on every interface."

Preferred:

```text
100.x.y.z:8788
```

Not:

```text
0.0.0.0:8788
```

Explicit LAN exposure remains a separate future/advanced choice with its own authorization and warning model.

## Availability and authority

Reachability and authority are separate.

Examples:

### On demand

```text
Relmote installed
Agent Access disabled

user chooses Enable Agent Access
→ bind Agent API to exact Tailscale address
→ create/approve scoped Agent grant
→ generate one-time pairing code

user chooses Disable Agent Access
→ revoke active Agent grants
→ stop Tailscale-bound Agent listener
```

### Timed or persistent support

Remote Support policy may be timed or enabled until manually disabled, but that does not imply Agent authority. Agent sessions still require their own explicit capabilities and revocation boundary.

## Shared machines

A machine may be reachable through Tailscale without the current operator being an administrator of the tailnet that owns it.

Relmote should treat this as a normal topology:

- direct Tailscale reachability may work;
- Tailscale Serve configuration may not be available;
- Relmote pairing and grants still apply;
- no re-enrollment into another tailnet should be required merely to use Relmote.

## SSH

Existing Tailscale SSH or ordinary SSH over the tailnet can run Relmote CLI commands without exposing the browser service.

Examples:

```text
relmote status
relmote diagnose network
```

Relmote does not configure SSH automatically.

## Future: rendezvous and relay

Direct Tailscale is a useful current transport, not the final multi-network design.

A future optional Relmote Hub/rendezvous layer may support:

1. authenticated outbound node enrollment;
2. presence and version coordination;
3. direct peer-to-peer connection negotiation;
4. private-network/LAN paths where available;
5. encrypted relay fallback when direct connectivity cannot be established.

The Hub must remain orchestration/reachability infrastructure rather than the root of target authority.
