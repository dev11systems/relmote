# Failure modes v0.1

Relmote should define safe behavior before defining every component.

## Compute board crashes

Expected:

- safety MCU times out heartbeat;
- target output disarms;
- all HID keys release;
- ARMED indication clears;
- physical STOP remains functional;
- compute may reboot independently.

## Compute board compromised

Assumption:

> network-facing Linux may eventually be compromised.

Mitigations:

- safety MCU accepts only bounded semantic commands;
- time-limited physical authorization;
- replay-resistant internal messages;
- no arbitrary raw HID path by default;
- safety MCU owns final output state.

## Safety MCU crashes

Expected:

- hardware design defaults target output to disabled;
- watchdog/reset attempts recovery;
- no stuck key state if electrically feasible;
- Linux reports safety-plane unavailable;
- no fallback that bypasses safety MCU.

## I/O board failure

Expected:

- core remains serviceable;
- replace daughterboard;
- no identity/keys permanently tied to I/O board.

## USB-C connector damage

Expected:

- replace I/O daughterboard;
- main compute/safety boards survive.

## Rear contact damage

Expected:

- snap modules unavailable/degraded;
- core standalone operation remains possible;
- replace rear contact board.

## Module short/overcurrent

Expected:

- per-module/current-limited rail trips;
- core remains powered;
- fault is reported;
- module capability withdrawn.

## Module firmware malicious

Expected:

- module capability does not become authorization;
- module does not gain safety-plane privilege;
- module data treated as untrusted;
- ability to power-cycle/isolate module where hardware permits.

## Battery failure/removal

Expected:

- externally powered operation remains possible;
- battery fault reported;
- unsafe charging disabled.

## Display failure

Expected:

- physical STOP still works;
- hardware safety indicator still communicates armed/fault state;
- companion/CLI may continue operation if explicitly authorized.

## Wi-Fi/BLE failure

Expected:

- USB/local/manual paths remain available;
- target interface does not depend on Internet connectivity.

## Main storage corruption

Expected:

- documented recovery path;
- safety MCU remains fail-closed;
- owner can reinstall without Dev11 cloud activation.

## Power brownout

Expected:

- output defaults safe;
- action is not silently replayed after reboot;
- incomplete action requires a fresh action ID/authorization.

## Thermal limit

Expected:

- throttle compute;
- reduce/stop charging;
- shed optional modules if needed;
- preserve safety plane;
- never prioritize AI inference over battery safety.
