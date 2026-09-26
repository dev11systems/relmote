# LAN Preview

The Cousin Preview should support a temporary **local-network controller** before full Relmote cryptographic pairing is finished.

This is a preview bridge, not the final pairing protocol.

## Browser flow

On the target computer:

```text
relmote serve --lan
```

Relmote creates:

- a random high-entropy bearer token;
- a temporary Observe-only support session;
- an expiry;
- a LAN listener.

It prints a URL such as:

```text
http://192.168.x.x:8787/?token=<random>
```

A controller on the same trusted local network opens that URL.

## Preview limitations

LAN Preview is:

- read-only;
- Observe-only;
- temporary;
- token-authenticated;
- explicitly enabled each run;
- not intended for Internet exposure.

It does not provide:

- arbitrary shell;
- write actions;
- unattended access;
- persistent pairing;
- public relay access.

## Token

The token must:

- be generated with a cryptographically secure random source;
- be difficult to guess;
- expire with the preview server;
- never be logged by request handlers;
- be revocable by stopping/revoking the preview.

The final Relmote pairing protocol will replace bearer-token LAN preview access.

## HTTP versus HTTPS

The short-term preview may use HTTP on a trusted LAN because locally generated TLS certificates create substantial usability/trust problems before pairing exists.

This means the bearer token and diagnostic data are **not protected against a hostile LAN observer**.

Therefore:

- use only on a trusted private LAN;
- do not use on public/cafe/hotel Wi-Fi;
- prefer an existing encrypted VPN/SSH tunnel if the LAN is untrusted.

Production LAN control should use authenticated encryption established by Relmote pairing.

## SSH

SSH is a separate useful preview path.

If the target already runs an SSH server, the user may authenticate with the OS's existing SSH mechanism and run:

```text
relmote status
relmote diagnose network
```

This does not mean Relmote implements its own SSH server.

Using the mature host SSH server avoids duplicating authentication/security machinery during the preview.

## Threat boundary

LAN reachability does not create write authority.

The preview server exposes only the explicitly implemented read-only API.
