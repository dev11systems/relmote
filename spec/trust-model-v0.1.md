# Relmote Trust Model v0.1 — Draft

## Principals

- ControllerPrincipal — cryptographic controller identity.
- NodePrincipal — cryptographic Relmote-node identity.
- GroupPrincipal — owner-defined set of principals.
- InvitationPrincipal — short-lived one-time support relationship.
- TargetPrincipal — identity/evidence representing a target system.

## Relationships

Paired means controller and node recognize one another. It does not imply target authority.

Owner may manage node trust configuration.

Maintainer may request/administer defined capability sets.

Guest/support is temporary or limited.

## Grant

A grant binds:

principal + node + target + capabilities + mode + time + optional task constraints.

## Authority does not transit automatically

If A trusts B and B trusts C, Relmote does not infer that A trusts C. Delegation must be explicit.

## Groups

Groups are policy convenience. Audit should still retain which concrete controller performed an action.

## High-impact administration

Future policy may require stronger approval for node identity reset, owner removal, firmware trust-root change, unattended-access expansion, or safety-policy modification.

## Compromise assumptions

Assume controller devices can be lost, Linux nodes can be compromised, third-party modules can be malicious, relay infrastructure can be observed/compromised, and AI planners can produce incorrect actions.

Authority should be compartmentalized accordingly.
