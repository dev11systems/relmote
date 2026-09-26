# Frontends

Relmote frontends are interchangeable views/controllers of one runtime.

## TUI + Web together

A terminal-launched Relmote can serve the web GUI simultaneously.

Example:

```text
target computer
│
├─ relmote runtime
│   ├─ TUI on local terminal
│   └─ Web UI on localhost
│
└─ Tailscale Serve
       │
       ▼
 remote browser
```

A local user may watch/control support in the TUI while an authorized helper uses the browser remotely.

This is a particularly useful support pattern.

## Shared events

Future runtime event stream:

- session started;
- helper connected;
- task created;
- observation arrived;
- proposal awaiting approval;
- proposal approved/denied;
- support disabled.

Every frontend subscribes to the same events.

## Local approval

A remote request might appear simultaneously:

### TUI

```text
A helper wants to edit README.md
[Review] [Deny]
```

### Desktop browser

Same request.

Whichever authorized local interface acts first resolves it.

## Interface-specific strengths

### TUI

- terminal;
- SSH;
- headless;
- low bandwidth;
- keyboard-first.

### Web

- phones/tablets;
- visual evidence;
- diffs;
- KVM;
- touch;
- accessibility technologies supported by browsers.

### CLI

- scripts;
- composability;
- automation;
- diagnostics.

None changes the underlying authorization model.
