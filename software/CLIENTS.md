# Client forms

Relmote should support several controller experiences over the same semantic API.

## iPhone / iPad

Native client priorities:

- BLE discovery/pairing;
- local Wi-Fi;
- clear node/target/path display;
- approvals;
- notifications for store-and-forward results;
- KVM view when available.

The app should not need privileged access to the target device.

## Android / GrapheneOS

Same core functions, with particular attention to:

- BLE;
- local network;
- background behavior that does not require invasive permissions;
- compatibility with GrapheneOS's permission model;
- no mandatory Google services.

## Web / PWA

A local web UI served by Relmote is valuable because it provides a near-zero-install controller.

Potential access:

```text
https://relmote.local/
```

or an authenticated local address.

Browser limitations mean native BLE/USB features should remain optional enhancements, not assumptions.

## CLI

Examples:

```text
relmote nodes
relmote status rm-7A21
relmote task rm-7A21 "inspect network"
relmote approve <proposal>
relmote revoke <session>
```

## TUI

A terminal dashboard can combine:

- node list;
- target/path;
- task conversation;
- proposal queue;
- events/log;
- STOP/revoke.

## Desktop

A desktop client may be useful primarily for:

- KVM/video;
- multi-node administration;
- development;
- high-bandwidth logs.

It should still use the same API rather than becoming a privileged special client.

## No mandatory Dev11 app

Third-party controllers should be possible.

The API/specification should be sufficient to build one without reverse engineering.
