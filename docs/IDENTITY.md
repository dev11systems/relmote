# Identity and ownership

Relmote identity should belong to the people and systems using it, not to a mandatory Dev11 account.

## Identity layers

Relmote distinguishes person/owner identity, controller identity, node identity, target identity, session identity, and task identity.

## Device-first identity

A controller or node should be able to generate its own cryptographic identity locally. A Dev11 account is not required.

## Person identity is optional

A person may group several controller devices, but nodes ultimately authorize concrete controller keys or owner-defined groups, not mutable display names.

## Controller groups

Owners may define local groups such as:

- my-devices
- family-support
- homelab-admins
- community-network-maintainers

A grant can target one controller, a group, or a one-time invitation.

## No omnipotent account requirement

Cloud sync may be convenient, but authority should remain exportable, inspectable, and revocable.

## Shared ownership

A node may have several owners/maintainers. Future policy may support multi-party approval for high-impact actions such as firmware trust changes or identity reset.

## Target identity

A known Relmote node is not automatically a known target. Target identity may derive from Agent identity, SSH host key, BMC identity, hardware evidence, user confirmation, or a composite.

Ambiguous target identity should reduce authority rather than silently reuse old grants.

## Key storage

Potential storage includes OS secure storage, hardware secure element, safety-MCU protected storage, encrypted local file, or removable owner token.

No single mechanism is required across every implementation.

## Owner control

Owners should be able to inspect trusted identities, export their own identity material safely, rotate keys, revoke controllers, reset a node deliberately, and operate without Dev11 infrastructure.
