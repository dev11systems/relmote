# Capability vocabulary

Relmote permissions are expressed as narrow capabilities rather than broad roles such as “admin.”

The initial vocabulary is intentionally small.

## Identity and observation

- `system.identify` — identify the target without modifying it.
- `observe.console` — receive console/text output.
- `observe.screen` — receive screen/video state.

## Human-interface input

- `input.keyboard` — emit keyboard input.
- `input.pointer` — emit pointer input.

## Shell and files

- `shell.read` — execute/read commands intended to observe state.
- `shell.write` — execute commands that may modify state.
- `file.read`
- `file.write`

## Network

- `network.inspect`
- `network.configure`

## Power

- `power.read`
- `power.control`

## Storage

- `storage.read`
- `storage.write`

## Firmware

- `firmware.read`
- `firmware.write`

## Privilege

- `privilege.elevate` — request/use elevated authority.

Possessing `privilege.elevate` does not imply any of the underlying write capabilities; both should be required when applicable.

## Rules

- Unknown capabilities fail closed.
- Grants bind capabilities to a target and operating mode.
- Grants may expire.
- Connectivity does not create capabilities.
- Transport discovery does not create capabilities.
- Capabilities should remain stable wire identifiers once released.
- More dangerous capabilities should remain separable rather than collapsing into a generic “operate” permission.
