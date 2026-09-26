# Platform support

Relmote's schemas and protocols are cross-platform.

Implementation support is developed through OS adapters.

## Reference platform: Linux

Linux is the first-class development target for the initial Software Preview.

Reasons:

- current real-world testers use Linux;
- strong local/remote administration primitives;
- open system interfaces;
- excellent SSH support;
- easier rapid iteration;
- aligns with early hardware/embedded targets.

This is sequencing, not a Linux-only product decision.

## Linux preview targets

Prefer broadly available interfaces:

- `/etc/os-release`;
- `/proc`;
- `/sys`;
- iproute2;
- lsblk/util-linux;
- systemd when present.

Gracefully degrade when a tool/subsystem is absent.

Do not require systemd merely to qualify as a Relmote Linux node.

## macOS

Planned native adapter:

- system identity;
- network configuration/routes;
- storage;
- processes/services;
- logs;
- launchd;
- native permissions.

Relmote protocols and controller UI remain the same.

## Windows

Planned native adapter:

- system identity;
- network configuration/routes;
- storage;
- processes/services;
- Event Log;
- PowerShell/native APIs where appropriate.

Windows-specific privilege/security semantics should be modeled explicitly rather than pretending they are POSIX.

## Compatibility principle

```text
Linux adapter ──┐
macOS adapter ──┼──► Relmote observation schemas
Windows adapter ┘
```

Diagnostics consume common semantics rather than hard-coding one OS wherever practical.

## Remote targets

SSH is especially natural for Linux/macOS.

Windows may use:

- OpenSSH when configured;
- native Relmote Agent;
- future Windows management adapter.

The transport does not define the platform.
