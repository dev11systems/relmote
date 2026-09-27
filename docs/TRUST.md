# Trust, permissions, and agency

Relmote is designed around a simple rule:

> **A communication path is not an authorization grant.**

Connecting to a device over USB, Bluetooth, Wi-Fi, Ethernet, mesh, or another bearer does not automatically authorize Relmote to operate it.

## Trust layers

Relmote distinguishes:

1. **Controller identity** — who is asking?
2. **Target identity** — which system will be affected?
3. **Session authority** — what may this session do?
4. **Action authority** — does this specific action fit the grant?
5. **Transport security** — is the path authenticated/encrypted enough for the requested capability?

## Capability grants

Permissions should be narrow and composable.

Example:

```text
target: home-server
expires: 30 minutes

allow:
  - observe.console
  - shell.read
  - diagnostics.network

ask:
  - shell.write
  - privilege.sudo

deny:
  - storage.erase
  - firmware.write
  - persistence.install
```

## Modes

### Observe

No target input.

### Teach

Relmote may reason about the state and explain suggested actions, but the human performs them.

### Assist

Relmote prepares actions and requires approval before execution.

### Operate

Relmote may execute automatically, but only inside a bounded capability grant with an expiry and identified target.

## Physical controls

The product should explore physical controls for:

- pairing;
- authorization;
- current operating mode;
- immediate stop / revoke;
- visible activity indication.

A physical stop must override software.

## No stealth mode

Relmote should not intentionally masquerade as an innocuous device to conceal control activity.

Its design should favor:

- visible status;
- inspectable sessions;
- explicit pairing;
- action logs;
- identifiable device names;
- short-lived authority.

## Privilege escalation

Relmote must never silently escalate privileges.

Elevated actions should be modeled explicitly as capability requests.

## Lost connectivity

Loss of the controller does not always require immediate termination: store-and-forward tasks may be intentional.

However, any autonomous continuation must be explicitly authorized in advance and bounded by:

- task;
- target;
- capabilities;
- time;
- resource limits;
- stop conditions.

## Uncertainty

When target identity, current state, or action consequences are ambiguous, the safe state is **do not execute**.


## External metadata disclosure

A transport can create privacy side effects even when the payload itself remains private.

Relmote must not silently enable a transport feature that publishes externally visible identifiers or other durable metadata as a side effect. Examples include:

- requesting a publicly logged TLS certificate;
- publishing a DNS name outside the user's private namespace;
- registering a device with a cloud relay/control service;
- creating a public ingress or forwarding rule;
- exposing a device or owner identifier to a third-party directory.

When such a feature is useful, Relmote should:

1. explain what metadata leaves the local/private environment;
2. identify whether the disclosure is public, third-party-visible, or merely tailnet-private;
3. require explicit human approval before activation;
4. offer a lower-disclosure transport when one exists;
5. avoid treating refusal as an error when another private path is available.

For Tailscale specifically, direct binding to the target's Tailscale address does not require public TLS certificate issuance. Tailscale Serve/HTTPS may provision a public-CA certificate whose fully qualified device name is recorded in Certificate Transparency logs. Relmote therefore treats Serve/HTTPS as optional, explicit convenience rather than an automatic prerequisite.
