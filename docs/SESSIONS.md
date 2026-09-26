# Sessions and execution semantics

A Relmote session binds one controller to one identified target with a bounded grant.

## Session state

A session currently carries:

- session ID;
- controller ID;
- target ID;
- operating mode;
- capability set;
- optional expiry;
- revocation state;
- approved action IDs;
- already-executed action IDs.

## One-time action identity

Every proposed action receives a unique `action_id`.

Once dispatched, that ID is recorded as executed. Replaying the same action ID is rejected.

This is important for intermittent or retried transports where the same message may arrive more than once.

## Approval

In Assist mode, an allowed action still cannot execute until its exact `action_id` is approved.

Approval is consumed when the action executes.

Revoking the session clears pending approvals.

## Expiry and revocation

Expired or revoked sessions cannot dispatch actions.

The eventual physical stop control should map to immediate session revocation at the safety plane and should not depend on the AI planner.

## Audit

The initial audit log records metadata such as:

- proposal;
- policy decision;
- approval;
- denial;
- execution;
- session revocation.

The controller intentionally does **not** put command payloads or typed text into the audit trail by default. Future logging policy may allow explicit opt-in payload capture.
