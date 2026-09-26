# Feature placement

Relmote should resist turning Pocket into a physical checklist of every use case.

## Base Pocket

Strong candidates for every reference Pocket:

- efficient node compute;
- independent safety MCU;
- Wi-Fi;
- BLE;
- two USB-C ports;
- replaceable battery;
- status display;
- AUTHORIZE;
- STOP;
- open snap interface;
- local storage;
- hardware safety indicators.

Possible but not yet mandatory:

- third USB-C expansion port;
- NFC pairing;
- microSD;
- basic USB serial.

## Snap modules

### Mesh

Potential:

- LoRa radio;
- MeshCore;
- Meshtastic;
- optional GNSS.

### Serial / Console

Potential:

- TTL UART;
- RS-232;
- RS-485;
- RJ45 console variants;
- galvanic isolation variant.

### KVM

Potential:

- HDMI input;
- USB target;
- video capture;
- optional passthrough;
- higher power budget.

### Ethernet

Potential:

- 1 GbE;
- optional PoE input;
- dock mode.

### Cellular

Potential:

- LTE/5G;
- GNSS;
- SIM/eSIM support as appropriate;
- external antenna option.

### Battery

Potential:

- larger capacity;
- power telemetry;
- downstream pass-through.

### Embedded/debug

Potential:

- SWD;
- JTAG;
- GPIO;
- I²C;
- SPI;
- target voltage sensing;
- optional level shifting/isolation.

### Storage / Recovery

Potential:

- removable storage;
- boot/recovery images;
- evidence vault.

### Radio experiments

Community modules might support:

- amateur-radio modem/TNC;
- 802.15.4;
- unusual physical links.

These should not bloat base Pocket.

## Software plugins

Strong plugin candidates:

- SSH;
- Redfish;
- AMT-class management;
- vendor device APIs;
- serial protocol decoders;
- KVM/video interpretation;
- planner providers;
- MeshCore;
- Meshtastic;
- notification integrations.

## All-in-One integration candidates

Native ports/features worth studying because field technicians use them frequently:

- Ethernet;
- serial;
- HDMI/KVM;
- larger battery;
- third USB-C;
- removable storage.

Cellular/LoRa may still be better modular even on All-in-One because radio requirements vary geographically and over time.

## Dock integration candidates

A desktop/server dock could provide:

- continuous power;
- Ethernet/PoE;
- HDMI/KVM;
- USB hub;
- serial;
- external storage;
- antennas.

Pocket snaps/docks into it and remains the identity/policy node.

## Anti-bloat rule

A feature should enter base Pocket only if it:

1. serves many use cases;
2. is difficult to add externally;
3. has acceptable idle power;
4. does not substantially complicate certification/repair;
5. remains useful for years.

Otherwise: **module or plugin.**
