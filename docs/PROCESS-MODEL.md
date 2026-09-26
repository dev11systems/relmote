# Relmote process model

Relmote should feel like **one application with multiple interfaces**, not several unrelated programs.

## Core model

```text
                         relmote
                            │
                    Relmote Runtime
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
       CLI                 TUI              Web/API
        │                   │                   │
 scripts / SSH       local terminal       browser / PWA
                                                │
                                          local or remote
```

All interfaces operate on the same:

- node identity;
- targets;
- sessions;
- grants;
- tasks;
- observations;
- proposals;
- audit state.

## Default interactive launch

When run in an interactive terminal:

```text
relmote
```

desired behavior:

1. start the local Relmote runtime;
2. start the TUI;
3. make the local web UI available;
4. show the web address under “Open in browser”;
5. keep remote exposure disabled unless configured/enabled.

Example:

```text
RELMOTE

This computer
Support: Off

> Check this computer
  Enable support
  Open web interface
  Projects
  Technical details

Web interface:
http://127.0.0.1:8787
```

## Browser controller

The same running Relmote may serve:

```text
127.0.0.1:8787
```

for a local browser.

If support/network exposure is explicitly enabled, an authorized remote browser may reach that same UI through:

- Tailscale;
- LAN;
- future Relmote P2P/relay.

No separate “web edition” is required.

## CLI

CLI commands talk to the same runtime/core.

Examples:

```text
relmote check
relmote status
relmote diagnose network
relmote support on
```

If a local runtime is already running, the CLI may eventually connect to it over a local IPC/API socket rather than creating independent state.

## TUI

The TUI is another controller of the runtime.

Actions performed in the TUI should immediately appear in the web UI and vice versa.

Example:

```text
iPad approves proposal
        ↓
runtime state changes
        ↓
TUI immediately shows:
APPROVED
```

## Headless mode

Servers can run:

```text
relmote agent --headless
```

with:

- no TUI;
- optional local API;
- optional configured private-network listener.

Administrators then use another Relmote controller or SSH CLI.

## Temporary mode

Portable preview:

```text
run binary
→ runtime + TUI + localhost web UI
→ quit
→ runtime exits
```

No permanent service.

## Installed mode

Persistent Agent:

```text
relmoted
     │
 background runtime
     │
 ┌───┼────────────┐
 CLI TUI        Web
```

Opening `relmote` connects to the existing local daemon.

## State consistency

Frontends must not each maintain independent authority state.

Bad:

```text
TUI thinks support is OFF
Web thinks support is ON
```

One runtime is authoritative.

## API boundary

The web API is not the “real” implementation with CLI/TUI bolted on.

Likewise the CLI is not privileged.

All frontends invoke the same semantic application layer.

## Principle

> **One Relmote, many views.**
