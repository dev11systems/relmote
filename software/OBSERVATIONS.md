# Observations, evidence, and uncertainty

Relmote separates:

- **task intent**;
- **proposed action**;
- **observation**;
- **interpretation**;
- **result**.

This prevents an AI interpretation from being confused with raw evidence.

## Observation

An observation records what a transport actually supplied.

Examples:

### Text

```yaml
kind: text
source: ssh
content: "eth0: link up"
truncated: false
```

### Screen

```yaml
kind: screen
source: kvm
frame_ref: ...
```

### Structured

```yaml
kind: structured
source: redfish
data:
  power_state: "On"
```

### No feedback

USB HID alone produces **no target observation**.

Typing a command is an action, not evidence that the command succeeded.

## Interpretation

A planner may derive:

```text
"DHCP appears to have failed."
```

from observations.

The interpretation should retain references to the evidence that supports it.

## Result

A task result can contain:

- findings;
- evidence references;
- uncertainty;
- actions performed;
- side effects;
- unresolved questions;
- requested capabilities.

## Truncation

Constrained transports may return summaries or partial evidence.

The controller should be able to distinguish:

```text
complete evidence
summarized evidence
truncated evidence
unavailable evidence
```

## Semantic compression

A remote node may transform large local evidence into a compact result:

```text
raw:
  180 KB logs

semantic result:
  link=up
  dhcp=failed
  attempts=3

evidence retained locally:
  yes
```

The summary is not falsely presented as the entire raw log.

## Provenance

Every observation should eventually carry enough provenance to answer:

- which node;
- which target;
- which system path;
- when;
- whether transformed;
- whether complete.
