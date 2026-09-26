# Discovery and addressing

Relmote discovery should work at several scopes.

## Nearby

Possible mechanisms:

- BLE advertisements;
- local USB;
- mDNS/DNS-SD on LAN;
- local Wi-Fi access point.

Nearby discovery may reveal only minimal information until pairing.

## Known nodes

A controller maintains owner-approved node identities.

A node can be reachable through changing transports without becoming a new identity.

```text
rm-7A21
├─ BLE nearby
├─ Wi-Fi LAN
├─ USB
└─ remote route
```

## Remote

Remote reachability may use:

- ordinary IP;
- user VPN;
- self-hosted rendezvous;
- future Unilink/Uniline integration;
- mesh gateways.

The Relmote protocol should not require a Dev11 relay service.

## Constrained/store-and-forward

A node may be:

- reachable only intermittently;
- reachable only through a low-bandwidth mesh;
- currently offline but expected later.

Discovery state should distinguish:

```text
online-interactive
online-constrained
store-and-forward
last-seen
unknown
```

## Identity

Human-friendly names are aliases.

The underlying node identity should be stable and cryptographic.

Example:

```text
friendly: dad-laptop-helper
node id:  rm:...
```

Renaming a Relmote must not change its trust identity.

## Target identity

Node identity and target identity are separate.

```text
Relmote rm-7A21
      │
      ├─ today → ThinkPad
      └─ later → router
```

A remembered Relmote does not imply remembered authorization for every target it touches.
