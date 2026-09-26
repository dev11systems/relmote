# Constrained Envelope v0.1 — Draft

This is the semantic envelope for carrying Relmote objects over constrained or store-and-forward links.

It is **not yet a LoRa/Meshtastic/MeshCore byte-level encoding**.

## Envelope

Logical fields:

```yaml
id: unique
kind: task | approval | status | result | event | evidence_ref
correlation: task/session/message id
priority: 0..100
expires: optional
payload: ...
```

## Priorities

Suggested convention:

```text
100 physical/safety control relay where applicable
 90 revoke / authorization
 80 interactive response
 70 task result
 50 normal task
 20 evidence chunk
 10 background sync
```

The exact queueing policy is transport-specific.

## Deduplication layers

Do not confuse:

### Delivery deduplication

“Have I seen this envelope?”

with:

### Action replay protection

“Has this target-changing action already been executed?”

An envelope may be retransmitted safely while the contained target action remains one-time.

## Compact encoding

Future wire encodings may use:

- CBOR;
- protobuf-like compact schemas;
- custom fixed-field framing only if justified.

Do not invent a bespoke encoding until real bearer limits are measured.

## Fragmentation

A bearer adapter may fragment one envelope.

Fragments need:

- envelope ID;
- index/count or offset;
- integrity;
- expiry;
- resumability.

Reassembly happens before semantic processing.

## Evidence references

Large evidence can remain remote:

```yaml
kind: evidence_ref
payload:
  evidence_id: obs-123
  size: 183421
  digest: ...
  completeness: complete
  retrieval:
    - wifi
    - usb
```

The constrained link can carry the finding without carrying 180 KB of logs.
