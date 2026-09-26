# Planner architecture

A planner turns human intent into proposed structured actions.

It does **not** own authorization or transports.

## Planner types

### Human

No AI.

The user directly selects/constructs actions.

### Deterministic automation

Known workflows, scripts, diagnostics, setup sequences.

### Local Relmote model

Small/offline model for:

- intent parsing;
- summarization;
- semantic compression;
- simple planning.

### Companion-hosted

A phone/tablet may run or broker the planner.

### Self-hosted

Home server/workstation.

### Cloud

Any supported provider chosen by the owner.

## Planner contract

Input:

```text
task
available capabilities
observations/results
policy-visible constraints
transport limitations
```

Output:

```text
proposal[]
explanation
required capabilities
expected observations
uncertainty
```

## No direct authority

A planner cannot:

- open `/dev/hidg0`;
- create a safety lease;
- grant itself capabilities;
- bypass STOP;
- silently change target identity.

The daemon/policy/safety plane mediate every action.

## Epistemic honesty

Planner context should explicitly represent unavailable feedback.

Example:

```json
{
  "target_feedback": "none",
  "system_transport": "usb.hid"
}
```

A planner must not pretend it observed command output through a blind transport.

## Provider neutrality

Relmote should not encode one vendor's API into core task semantics.

Provider adapters translate between:

```text
Relmote planner contract
        ↕
provider-specific API
```

This supports local/open models and future providers without redesigning authorization.
