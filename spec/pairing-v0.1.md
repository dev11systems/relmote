# Relmote Pairing v0.1 — Draft

Pairing establishes durable cryptographic identity relationships.

It does not automatically establish target authority.

## Node identity

A node generates/holds its own long-lived identity key material.

Human-friendly names are aliases.

```text
name: cousin-laptop
identity: rm:...
```

Renaming does not alter identity.

## Controller identity

Controllers also have cryptographic identities.

One person may own several controller devices.

Future account/sync systems may help manage them, but the protocol should not require a Dev11 account.

## Local pairing

Preferred methods may include:

- QR code;
- short authentication string;
- NFC-assisted initiation;
- USB;
- BLE with explicit local confirmation.

The user should be able to compare/confirm identities through an authenticated local ceremony.

## Remote invitation

For one-time support:

```text
node creates invitation
        ↓
user sends QR/link/code
        ↓
controller connects
        ↓
node/user confirms request
        ↓
temporary relationship
```

Invitation properties:

- short expiry;
- one-time or bounded use;
- node identity binding;
- maximum requestable capability envelope;
- no reusable node private secret.

## Pairing versus grant

```text
PAIRED
"Rae's iPad is a known controller."

GRANT
"Rae's iPad may inspect network state on this target
 for 30 minutes."
```

These must remain separate.

## Revocation

The node owner can revoke a controller identity.

Revocation prevents new sessions and should terminate sessions according to policy.

## Recovery

Owner recovery must not depend exclusively on a Dev11 cloud account.

Recovery design remains open, but candidate mechanisms include:

- local recovery key;
- owner-exported encrypted identity backup;
- hardware recovery path;
- re-pairing after deliberate node identity reset.

## Key rotation

Nodes/controllers should support key rotation without silently transferring authority to a different identity.

The exact cryptographic protocol is not frozen.
