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


## Network exposure

The ordinary path should not require users to reason about bind addresses, but Relmote should also avoid silently broadening network exposure.

Current direction:

1. keep underlying Relmote services loopback-only by default;
2. use an explicit private transport such as Tailscale Serve for ordinary remote access where available;
3. do not use public Funnel exposure by default;
4. do not silently fall back to all interfaces (`0.0.0.0`);
5. require an explicit action for trusted-LAN/all-interface exposure;
6. show the actual reachable private endpoint and whether temporary controller authentication/pairing is active.

Agent API and human controller exposure are separate surfaces and may use different credentials/policies.

The TUI/web controller should explain the active exposure path in plain language.
