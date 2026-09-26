# Relmote interfaces

Relmote is not defined by one user interface.

The same node/task/policy/evidence core should support several first-class controller surfaces.

## Web / GUI

Best for:

- nontechnical users;
- phones/tablets;
- visual diagnostics;
- permission prompts;
- screen/KVM;
- reviewing diffs.

## TUI

A terminal user interface is a **first-class Relmote interface**, not a debug fallback.

Best for:

- Linux;
- SSH sessions;
- headless systems;
- recovery environments;
- low-bandwidth links;
- keyboard-first operation;
- portable single-binary use.

Desired launch:

```text
relmote
```

when an interactive terminal is detected.

Example:

```text
┌─ RELMOTE ───────────────────────────────────┐
│ Cousin's Computer                           │
│                                             │
│ Support: ● ON                               │
│ Connection: Private                         │
│                                             │
│ > Check this computer                       │
│   Diagnose network                          │
│   View storage                              │
│   Projects                                  │
│   Stop support                              │
│                                             │
│ Recent                                      │
│ ✓ No failed services                        │
│ ⚠ Storage 91% used                          │
│ ○ Internet not tested                       │
│                                             │
│ [Enter] Select    [?] Help    [q] Quit      │
└─────────────────────────────────────────────┘
```

The default TUI should use plain language.

Technical details live behind a Details view.

## CLI

CLI is ideal for:

- scripts;
- automation;
- SSH;
- diagnostics;
- composability;
- debugging;
- advanced users.

Examples:

```text
relmote status
relmote check
relmote diagnose network
relmote support on
relmote support off
relmote workspace ...
```

CLI output should support:

- human-readable default;
- JSON for automation;
- stable exit codes.

## API

The semantic API powers all interfaces.

No UI gets a privileged bypass.

```text
Web ─┐
TUI ─┼──► Relmote API/core ──► policy/tasks/transports
CLI ─┤
API ─┘
```

## Interface parity

Interfaces need not expose every feature simultaneously, but equivalent operations should preserve the same:

- identity;
- grants;
- approvals;
- task IDs;
- evidence;
- audit semantics.

## Headless target

A Relmote Agent can run with no GUI.

Administrators may use:

```text
SSH → relmote TUI
```

or:

```text
SSH → relmote CLI
```

without enabling a browser service.

## Low bandwidth

TUI/CLI should remain usable when rich web UI/KVM is impractical.

This makes them especially important for:

- remote servers;
- serial consoles;
- mesh links;
- constrained field environments.

## Accessibility

TUI is not automatically accessible merely because it is text.

Design for:

- predictable keyboard navigation;
- no color-only meaning;
- screen-reader-friendly CLI alternative;
- reduced animation;
- copyable text;
- understandable focus state.

## Principle

> **Choose the interface that fits the situation; do not change the Relmote trust model to fit the interface.**
