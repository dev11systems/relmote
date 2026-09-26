# Relmote Pocket antenna/RF study v0.1

**Status:** layout constraints before RF simulation/testing.

## Base radios

Pocket is expected to include at least:

- Wi-Fi;
- Bluetooth/BLE.

LoRa, cellular, 802.15.4, GNSS, and other radios may remain optional modules.

## Base antenna zone

Reserve the top ~15–20 mm of the Pocket core as the primary RF region.

Avoid placing directly adjacent:

- snap magnets;
- large ground-connected metal structures;
- battery foil edge;
- switching inductors;
- high-current power paths;
- high-speed connector cages.

## Why modules complicate RF

A rear module can alter:

- antenna detuning;
- ground plane;
- user-hand interaction;
- radiation pattern;
- noise floor.

Therefore the module descriptor may eventually need RF metadata such as:

```yaml
rf:
  bands:
    - 915mhz
  antenna:
    type: onboard
  keepout_zone: top
```

This is exploratory; do not freeze descriptor fields yet.

## Radio modules

Radio modules should ideally carry their own antenna system unless the core provides a deliberately standardized RF connector/path.

Avoid a proprietary hidden antenna-sharing system.

Possible external antenna options:

- module-integrated antenna;
- documented u.FL/MHF-class internal connector;
- external SMA-style connector on field modules;
- USB-C external radio.

## Magnets

Magnet placement must be validated against:

- antenna performance;
- GNSS;
- magnetometer/compass if present;
- NFC if present.

Do not finalize magnet grade/geometry from mechanical retention testing alone.

## Cellular

Cellular is particularly likely to remain an L module or All-in-One feature because it adds:

- antenna volume;
- certification complexity;
- high transmit-current peaks;
- SIM/eSIM considerations;
- thermal load.

Keeping it modular protects the Pocket core from unnecessary complexity.

## NFC

NFC could be useful for:

- local pairing initiation;
- reading a node identity;
- opening a companion UI.

If added, coil placement must be coordinated with:

- magnets;
- rear modules;
- metal midframe;
- battery.

NFC should not itself grant privileged operation.
