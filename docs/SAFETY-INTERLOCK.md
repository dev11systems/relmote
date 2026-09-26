# Safety interlock

Relmote now models two independent stop paths.

## 1. Session stop

The controller provides every transport with a live `ExecutionContext`.

A long-running transport can repeatedly evaluate:

```text
context.should_stop()
```

This becomes true when the session is revoked or expires.

Therefore authorization is not checked only once at the beginning of an action.

## 2. Physical output gate

Target-facing HID additionally requires a `SafetyGate`.

The gate:

- starts disarmed;
- can be armed only for a finite lease;
- automatically disarms when the lease expires;
- supports a latched STOP;
- refuses to re-arm while STOP remains latched;
- remains disarmed after STOP is reset.

Resetting STOP and authorizing output are deliberately two separate state transitions.

## Combined rule

For target output to continue:

```text
session remains authorized
          AND
physical output gate remains armed
```

Either side can stop the operation.

```text
          session revoke / expiry
                    │
                    ▼
controller ──► ExecutionContext
                    │
                    ├──── STOP
                    ▼
               HID transport
                    ▲
                    ├──── STOP
                    │
              SafetyGate
                    ▲
                    │
              physical control
```

## Replay behavior

Once an action has been handed to a target-side transport, its action ID is consumed even if:

- STOP interrupts it;
- the session is revoked part-way through;
- the transport reports an uncertain/partial result.

Relmote does not automatically replay partially emitted actions. A new attempt requires a new proposal/action ID.

## v0.1 versus final architecture

The Pi-only prototype validates these semantics in software.

The intended later architecture moves the physical gate and target-facing interface to a separate safety MCU, making STOP independent of the high-level Linux/agent process.
