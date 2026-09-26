# Store-and-forward

Relmote should work when a live interactive session is impossible.

## Example

A controller submits:

```text
When router-01 becomes reachable:
- inspect interface state
- inspect DHCP state
- read only
- do not reboot
- return a compact summary
- expire in 6 hours
```

The task may cross:

```text
phone
  ↓ BLE
local mesh node
  ↓ LoRa / MeshCore
remote Relmote
  ↓ UART
router
```

The phone may disappear before execution.

## Requirements

A store-and-forward task needs explicit:

- target;
- expiry;
- capabilities;
- autonomous-continuation permission;
- resource limits;
- result return policy.

## Queue priorities

Candidate priorities:

```text
emergency-stop/control
authorization
interactive
task result
normal task
bulk evidence
background sync
```

STOP/revoke traffic must not sit behind a bulk log transfer.

## Delivery

Messages should support:

- unique IDs;
- acknowledgement;
- expiry;
- retry;
- deduplication;
- chunking;
- resumability.

Retrying message delivery must not imply replaying a target-side action.

## Evidence locality

On constrained links, large evidence may remain on the remote Relmote.

The controller receives:

- summary;
- evidence metadata;
- digest/reference;
- retrieval options when a richer path becomes available.

## Return path

The result need not return over the same bearer.

```text
task sent: LoRa
result returned later: Wi-Fi
```

Relmote identity/task identity preserves continuity across that change.

## No hidden autonomy

Store-and-forward is not a blanket permission for the agent to continue indefinitely.

The grant is bounded by task, capabilities, target, time, and resource limits.
