# Software-first MVP

The first deployable Relmote is a **local software node**.

## S1

Run:

```bash
relmote serve
```

Then open the printed localhost URL.

S1 intentionally provides only read-only portable observations:

- identity;
- OS/platform;
- memory;
- storage;
- basic network information.

## Security boundary

S1 binds to loopback only.

It will reject:

```text
0.0.0.0
LAN address
public address
```

because controller authentication/pairing is not implemented yet.

This is deliberate.

## Why start here?

S1 proves:

- Relmote can be useful without hardware;
- the browser can be the first controller;
- the semantic capability model maps to native software observations;
- no cloud account is required;
- deployment can be temporary.

## S2

Next:

- real node identity;
- sessions in the browser UI;
- task/proposal/observation model;
- richer portable diagnostics;
- PWA assets;
- packaged ephemeral launch.

## S3

Only after pairing/authentication:

- LAN binding;
- second-device browser controller;
- QR/fingerprint pairing.

## Temporary use

The desired eventual experience is approximately:

```text
download/run Relmote
→ browser opens
→ use support session
→ stop Relmote
→ no persistent service unless explicitly installed
```
