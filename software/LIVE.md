# Relmote Live

Relmote Live is a temporary boot/recovery environment implementing a Relmote node.

## Purpose

Provide rich native diagnostics when the normal OS does not boot, should not be modified, cannot run Agent, or is being recovered.

## Potential forms

- bootable USB;
- bootable SD;
- network boot;
- owner-selected recovery partition.

## Capabilities

Potential read-only defaults:

- hardware inventory;
- disk health;
- filesystem inspection;
- network diagnostics;
- backup/export;
- boot configuration inspection.

Write/repair operations require explicit capabilities.

## Relationship to Pocket

Pocket may provide controller path, physical authorization, boot selection through KVM/HID, and a network path to Live.

Once Live boots:

```text
before:
Pocket → HID/KVM

after:
Pocket → USB/LAN → Relmote Live
```

The same task can upgrade to the richer path.

## Persistence

Live should default toward temporary operation and should not install itself into the target OS unless explicitly requested.
