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
