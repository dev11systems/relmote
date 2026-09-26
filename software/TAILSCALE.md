# Tailscale integration

Tailscale is an optional **reachability adapter** for Relmote.

It does not replace Relmote identity, session policy, capabilities, or evidence.

## Preferred preview pattern: localhost + Tailscale Serve

Keep Relmote bound to localhost:

```text
relmote serve
→ 127.0.0.1:8787
```

Then publish that local service privately through Tailscale Serve.

Conceptually:

```text
Relmote
127.0.0.1:8787
      │
Tailscale Serve
      │
encrypted tailnet
      │
controller browser
```

Advantages:

- Relmote itself remains localhost-only;
- Tailscale provides encrypted reachability;
- tailnet access controls apply;
- no public Internet listener;
- Relmote does not need to discover/bind a specific VPN interface.

Exact Tailscale CLI syntax can vary by installed version; use current Tailscale documentation.

## Direct Tailscale-IP binding

Relmote may also support binding directly to a user-specified Tailscale address.

This is useful when:

- Serve is unavailable;
- the user wants direct port access;
- another reverse proxy/service manager is used.

Prefer explicit:

```text
--bind <tailscale-ip>
```

rather than listening on every interface.

## Availability

Tailscale reachability and Relmote availability are separate.

Examples:

### On demand

```text
Relmote installed
support disabled

user chooses Enable Support
→ start Relmote listener/Serve

user chooses Disable Support
→ revoke sessions
→ stop exposure
```

### Timed

Enable for:

- 15 minutes;
- 1 hour;
- custom duration.

### Persistent

Explicit:

```text
Until manually disabled
```

Useful for trusted family support or infrastructure.

## Grants

Persistent Tailscale reachability does not require persistent authority.

Example:

```text
Rae controller:
  diagnostics.read      always allowed
  logs.read             always allowed
  screen.observe        ask
  keyboard.input        ask every session
  system.write          deny
```

## SSH

Existing Tailscale SSH or ordinary SSH over the tailnet can run Relmote CLI commands without exposing the browser service.

Examples:

```text
relmote status
relmote diagnose network
```

Relmote does not configure SSH automatically.

## Future

Once Relmote pairing is implemented, the browser/API should authenticate the Relmote controller identity even when Tailscale already authenticated network membership.

Defense in depth:

```text
Tailscale:
may this device reach this service?

Relmote:
which controller is this and what may it do?
```
