# Pairing UX

Pairing should establish **known identity**, not blanket remote control.

## Local pairing

Example Pocket flow:

1. Controller discovers nearby node.
2. Pocket displays a short fingerprint and/or QR.
3. Controller displays the same fingerprint.
4. Human confirms the match.
5. Controller and node become paired.

Example:

```text
Pocket:
PAIRING
7A2F-91C0-4B11-88DE

Controller:
Pair with "Pocket"?
Fingerprint:
7A2F-91C0-4B11-88DE

[ Confirm ]
```

Production pairing should use an authenticated key-agreement protocol. The current Python pairing-code model is only scaffolding.

## What pairing grants

By itself:

```text
✓ recognize controller
✓ permit future session requests
```

Not:

```text
✗ keyboard control
✗ shell
✗ files
✗ unattended access
```

Those require grants.

## One-time support

A target user may create a temporary invitation instead of durable pairing.

## Controller replacement

A new phone/tablet receives a new controller identity unless the owner deliberately restores/transfers identity.

## Visible identity

Controller UI should show both:

- friendly name;
- short fingerprint.

This helps distinguish two devices with the same name.

## Physical node pairing

Pocket should require local physical presence for first-owner pairing unless deliberately placed into another enrollment mode.

## Software Agent pairing

Agent can show:

- QR;
- short code/fingerprint;
- local OS confirmation dialog.

Headless servers may use CLI confirmation.

## No QR-as-secret assumption

QR codes are a transport for pairing data, not a security primitive by themselves.
