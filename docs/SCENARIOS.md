# Scenarios

These scenarios are design probes, not promises that every path will exist in the first hardware revision.

## Phone beside a broken PC

```text
phone
  │ BLE
Relmote
  │ USB HID
PC
```

The phone is the cockpit. Relmote can type into the PC, but without another feedback path it is blind.

Add a KVM module:

```text
phone
  │ BLE
Relmote
  ├─ USB HID → PC
  └─ HDMI ←── PC
```

Now it can reason over visible state.

## Tablet supervising a headless Linux system

```text
iPad
  │ local Wi-Fi
Relmote
  │ SSH
Linux host
```

Because SSH is already available and authorized, Relmote uses the native text interface rather than keyboard emulation.

## Android/GrapheneOS phone and a router console

```text
GrapheneOS phone
      │ BLE
   Relmote
      │ UART / console cable
    router
```

Useful when the router's IP networking is broken.

## Remote constrained mesh

```text
controller
   │
mesh node )))))) LoRa / mesh )))))) remote node
                                      │
                                   Relmote
                                      │
                                    serial
                                      │
                                    target
```

The controller sends a compact, bounded diagnostic task. Relmote performs it locally and returns a structured summary rather than streaming a terminal session.

## Store-and-forward

A task can be authorized before the controller disconnects:

```text
When target becomes reachable:
- inspect disk health
- read only
- summarize failures
- expire in 6 hours
```

Relmote waits, performs the task inside the grant, and returns the result when any allowed controller path becomes available.

## Relmote-to-Relmote

```text
operator
  │
Relmote A
  │ changing communications paths
Relmote B
  │
target
```

This allows the protocol to preserve intent while individual bearers change or disappear.

## Family/support scenario

A trusted person plugs Relmote into a machine they want help with. Pairing and target authorization occur locally; the remote helper receives only the capabilities granted for that session.

The design goal is to make remote help possible without converting the target into a permanently managed machine.
