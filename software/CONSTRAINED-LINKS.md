# Constrained links

Relmote should degrade **semantics**, not merely run ordinary broadband protocols badly.

## Link properties

A controller path may report:

- bandwidth;
- latency;
- interactive/noninteractive;
- metered status;
- maximum payload;
- reliability;
- store-and-forward support.

## Link profiles

### Rich

Examples:

- Ethernet;
- Wi-Fi;
- USB networking.

Can carry:

- KVM/video;
- full logs;
- files;
- interactive shells.

### Interactive constrained

Examples:

- some mesh links;
- slow radio/IP paths.

Prefer:

- text;
- structured state;
- compact events;
- compressed evidence.

### Store-and-forward constrained

Examples:

- very low-rate LoRa;
- intermittent relay.

Prefer:

- task envelopes;
- approvals;
- status;
- semantic results;
- hashes/references.

## Adaptation

A task like:

```text
diagnose network
```

does not change meaning.

Its representation/result strategy does:

```text
Rich:
  stream terminal + logs

Constrained:
  execute locally
  return structured findings

Very constrained:
  return status code + tiny evidence summary
  retain raw evidence locally
```

## User visibility

The controller should show when it is operating in a degraded link mode.

Example:

```text
PATH: MeshCore / LoRa
mode: constrained
estimated task payload: 3 messages
raw logs: retained remotely
```

## Safety

Constrained links make acknowledgement ambiguous.

Therefore:

- target-changing actions use action IDs;
- action execution and message delivery are separate concepts;
- missing ACK does not automatically cause target-action replay.
