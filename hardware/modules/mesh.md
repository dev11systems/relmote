# Mesh module

**Likely class:** S

## Purpose

Provide constrained/off-grid controller transport.

Potential radios/protocols:

- LoRa;
- MeshCore;
- Meshtastic.

## Capabilities

Possible descriptor capabilities:

```text
radio.lora
mesh.meshcore
mesh.meshtastic
```

## Architecture

The module should carry its own RF front end and antenna strategy.

Relmote sees a controller transport with properties such as:

```text
interactive: maybe
constrained: yes
store_forward: yes
bandwidth: low
```

## Why module?

- regional frequencies;
- antenna needs;
- evolving radio hardware;
- not every user needs it;
- preserves Pocket RF simplicity.

## Power

Low average power may hide transmit peaks. Descriptor must report both.

## Trust

Incoming mesh data is untrusted controller-path traffic and passes through normal pairing/authentication/policy.
