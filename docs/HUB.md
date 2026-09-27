# Relmote Hub

The **Relmote Hub** is an optional self-hosted orchestration and rendezvous layer for people who manage more than one authorized Relmote node or Agent Host.

The Hub is a role, not a special appliance and not the root of trust.

## Role separation

Relmote distinguishes:

- **Controller** — human-facing interface for observation, approval, and revocation;
- **Agent Host** — compute/runtime that executes agent tooling and adapters;
- **Target / Node** — the system-side authority boundary;
- **Hub** — orchestration, inventory, presence, rendezvous, and coordination across many roles.

These roles may run on separate machines or share one host.

A common self-hosted deployment is expected to be:

```text
                  one self-hosted machine
             ┌────────────────────────────┐
Controller ─►│ Relmote Hub                │
             │ Agent Host                 │
             │ optional MCP/Codex adapter │
             └─────────────┬──────────────┘
                           │
                    private transport
                           │
             ┌─────────────┼─────────────┐
             ▼             ▼             ▼
          Target A      Target B      Target C
```

Co-location reduces operational friction, but does not collapse the roles semantically.

## Why co-locate Hub and Agent Host

For a single-user or household/self-hosted deployment, the machine already providing agent compute is often the natural place to run the Hub because it is likely to be:

- online more often than a phone/tablet;
- already trusted to hold Agent Host configuration;
- capable of running local web/CLI services;
- suitable for update coordination and background presence;
- a convenient place for future MCP/Codex adapters;
- able to broker or relay sessions without requiring the Controller to remain open.

This is a deployment convenience, not an architectural requirement.

A Hub may also run:

- on a dedicated server;
- in a VM/container;
- on a NAS/home server;
- separately from all Agent Hosts;
- on a machine that is also a Relmote Target, if deliberately configured.

## What the Hub may know

The Hub may maintain durable orchestration metadata such as:

- node/Agent Host identity and friendly name;
- online/offline/presence state;
- Relmote version and exact build identity;
- platform/architecture;
- supported transports and capabilities;
- tags/groups;
- last-seen timestamps;
- pending update availability;
- active session summaries;
- attention/diagnostic summaries.

This is enough to answer operational questions such as:

- Which machines need an update?
- Which Agent Hosts are online?
- Which path can reach this target?
- Which sessions are active?
- Which target needs human approval?

## What the Hub must not implicitly gain

Connecting a node to a Hub must not grant the Hub blanket target authority.

In particular, the Hub should not automatically gain:

- filesystem access;
- terminal access;
- screen access;
- persistent Agent bearer credentials;
- administrative privileges;
- the ability to mint target grants;
- authority merely because it can relay packets.

Target grants remain target-issued, scoped, visible, and revocable.

If the Hub and Agent Host share a machine, process co-location must not be treated as permission inheritance.

## Credential boundary

Near-term paired-target profiles belong to the Agent Host layer.

The Hub should prefer metadata references such as:

```text
target identity
paired: yes/no
agent host: host-a
available capabilities
session state
```

rather than copying bearer credentials into a central Hub database.

When an operation requires target authority, the Agent Host or another explicitly authorized component should consume the scoped credential.

Longer term, credentials should move into OS keyrings or another local secret store with process-scoped access.

## Initial Hub MVP

The first useful Hub does not need to be a full RMM platform.

A minimal self-hosted Hub can begin as a local/private inventory and coordination service with:

1. **Node inventory**
   - identity;
   - online state;
   - version/build;
   - platform/architecture;
   - transports/capabilities.

2. **Agent Host inventory**
   - online state;
   - detected tools/capabilities;
   - current load/availability;
   - locally paired target references.

3. **Version coordination**
   - current build per node/host;
   - update available;
   - update selected/all nodes;
   - staged/canary update support later;
   - restart-required/session-impact warnings.

4. **Session overview**
   - pending approvals;
   - active grants;
   - revocation controls;
   - session/transport health.

5. **Rendezvous**
   - allow nodes and Agent Hosts to find each other;
   - prefer direct private-network paths;
   - do not make relay synonymous with authority.

This MVP can run on the same machine as the Agent Host.

## Enrollment direction

For MSP-style or remote-new-machine workflows, the eventual Hub should support outbound enrollment.

Conceptually:

```text
new target
   │
   │ outbound authenticated enrollment/presence
   ▼
Relmote Hub / rendezvous
   ▲
   │
Agent Host / Controller
```

This avoids requiring the operator to manually configure inbound NAT, certificates, or per-target reverse proxies.

Enrollment should establish identity and reachability, not blanket control. Sensitive operations still require target policy and grants.

## Connection selection

The Hub may help select a path, for example:

```text
direct Tailscale/private IP
        ↓ unavailable
direct LAN/private route
        ↓ unavailable
P2P/rendezvous-assisted path
        ↓ unavailable
encrypted Hub relay
```

Transport choice must respect the privacy rule in [TRUST.md](TRUST.md): Relmote must not silently create public metadata side effects or public ingress.

## Relay

A future Hub relay may carry encrypted Agent/terminal/screen traffic when direct paths fail.

Relay does not make the Hub the authority boundary.

Prefer end-to-end authenticated/encrypted sessions where the relay cannot broaden capabilities or forge target approval.

## Failure and independence

Nodes must remain usable without the Hub.

If the Hub is offline:

- local Controller workflows should still work;
- direct Agent Host ↔ Target paths should still work where possible;
- existing target authority should not change;
- a node must not become unmanaged or locked out merely because orchestration disappeared.

## Multi-Hub / portability direction

The architecture should not make one permanent Hub instance part of device identity.

A future deployment may move the Hub, run a backup Hub, or operate multiple administrative domains without re-defining target ownership.

Hub migration must not silently broaden authority.

## Relationship to the Agent Host validation milestone

The current priority remains validating the real Controller → Agent Host → Target path.

Hub implementation should reuse the same:

- target identity;
- paired-target service boundary;
- capability vocabulary;
- session model;
- transport discovery;
- revocation semantics.

The Hub should coordinate those primitives rather than invent a second authorization model.
