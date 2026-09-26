# Remote support UX

The remote-support controller should converge on a small set of understandable surfaces.

## Controller navigation

```text
Overview
Screen
Terminal
Files
Diagnostics
Activity
```

Only available/authorized surfaces are enabled.

## Overview

Show:

- target identity;
- connection status;
- support availability;
- active grants;
- attention items;
- active screen/terminal sessions.

## Screen

Separate:

- view screen;
- keyboard/mouse control.

Never imply control merely because viewing is active.

## Terminal

Show authority plainly:

```text
Terminal
User: target-user
Privilege: normal user
Workspace restriction: none
```

Administrative escalation is a separate action/policy decision.

## Files

Workspace-scoped file access, proposals, diffs, and approvals.

## Diagnostics

Plain-language findings first, evidence/details second.

## Activity

Show meaningful events:

- helper connected;
- screen sharing started/stopped;
- control granted/revoked;
- terminal opened/closed;
- file proposal approved/denied;
- support disabled.

## Target-side visibility

The target must be able to answer at a glance:

> Who is connected, what can they do, and how do I stop it?

Example:

```text
REMOTE SUPPORT — ON

1 helper connected

Active now:
  Screen viewing
  Terminal (normal user)

Control:
  Keyboard/mouse OFF

[ STOP SUPPORT ]
```


## Automatic network exposure

The ordinary path should not require users to understand bind addresses.

On Linux preview startup:

1. if Tailscale is connected with a usable IPv4 address, bind the web controller only to that Tailscale address;
2. otherwise remain localhost-only;
3. never silently fall back to all interfaces (`0.0.0.0`);
4. require explicit selection for LAN/all-interface exposure.

Until Relmote controller pairing is implemented, non-local web exposure also uses a random per-run access token.

The TUI must display the actual reachable URL and exposure description.
