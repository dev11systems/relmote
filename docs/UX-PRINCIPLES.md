# Relmote UX principles

Relmote may be technically sophisticated. **Using it should not require understanding that sophistication.**

## Primary principle

> The common path should be understandable without IT, networking, security, or software-engineering expertise.

Complexity is progressively disclosed.

## Two layers

### Everyday view

Use human concepts:

- This computer
- Your helper
- Support is on/off
- What they can see/do
- Ask me before changes
- Stop support

Avoid requiring users to understand:

- ports;
- IP addresses;
- SSH;
- NAT;
- bearer tokens;
- capability identifiers;
- keypairs;
- transport selection;
- workspace policy syntax.

### Advanced view

For people who want it, expose:

- paths/transports;
- node IDs/fingerprints;
- Tailscale/WireGuard;
- SSH;
- capability IDs;
- logs/evidence;
- interface binding;
- policy details;
- self-hosting;
- developer tools.

Advanced controls should not be required to accomplish ordinary support.

## First-run target

Desired temporary-support flow:

```text
Download / open Relmote
        ↓
"This computer"
        ↓
[ Get Help ]
        ↓
Choose helper / share invitation
        ↓
Relmote clearly shows requested access
        ↓
[ Allow ]  [ Not now ]
        ↓
support
        ↓
[ Stop Support ]
```

## Installed support flow

```text
Relmote
Support: OFF

[ Enable Support ]

Who can help:
  Rae

When support is enabled:
  ✓ system diagnostics
  ? ask before making changes

[ Disable Support ]
```

No reinstall should be necessary to turn support back on.

## Language

Prefer:

```text
"View system information"
```

over:

```text
system.identify
```

Prefer:

```text
"Rae wants to edit README.md"
```

over:

```text
workspace.file.write capability request
```

Technical identifiers remain available in details.

## Permission prompts

A prompt must answer:

1. Who is asking?
2. What do they want to do?
3. Where?
4. For how long?
5. What could change?
6. How do I stop it?

Example:

```text
Rae wants to edit one file

Project:
  Test Website

File:
  README.md

You'll see the proposed change first.

[ Review Change ]  [ Deny ]
```

## Defaults

Safe defaults should also be convenient defaults.

Examples:

- temporary mode rather than background service;
- Observe before Operate;
- private network rather than public listener;
- ask before writes;
- no arbitrary shell by default;
- clear Stop Support control.

Do not make users weaken security just to make Relmote usable.

## Errors

Errors should lead with recovery:

Bad:

```text
SSH exit 255
```

Better:

```text
Relmote couldn't reach the other computer.

Check that:
• it is online;
• Tailscale is connected;
• remote support is enabled.

Technical details ▸
```

## Progressive disclosure

Every technical screen should have a useful simple summary.

Example:

```text
Connection
✓ Private and encrypted

Details ▸
  Tailscale
  100.x.x.x
  SSH host key ...
```

## Installation

The target experience should become:

### Windows

Download → open → confirm OS security prompt → Relmote.

### macOS

Download → open → Relmote.

### Linux

Package/AppImage or similarly simple supported package → Relmote.

Command-line installation remains available for technical users.

## No mandatory account

Do not require account creation before someone can receive local/one-time support.

An optional account may provide convenience such as controller sync, but must not be the usability tax for basic operation.

## Accessibility

- keyboard navigable;
- screen-reader semantics;
- large primary controls;
- do not rely on color alone;
- reduced motion;
- plain-language labels;
- concise default screens;
- technical detail expandable;
- avoid time-pressure UI unless expiration is genuinely required.

## Supporter UX

The helper should also get a coherent view:

```text
Cousin's Computer
Connected privately

You can:
✓ view diagnostics
✓ inspect Test Project

Ask first:
? edit files
? run project tools

Unavailable:
– system administration
```

The helper should not need to mentally reconstruct policy from error messages.

## Design test

Before adding a user-facing feature, ask:

> Could a nontechnical family member correctly understand what this does and how to stop it?

If not, the interaction needs another design pass.
