# Terminal

Terminal access is a first-class Relmote controller surface and capability.

## Distinctions

Do not collapse these into one permission:

### Observe command output

Run named diagnostic operations and return output.

### Workspace execution

Run approved project tools inside a configured workspace.

### Interactive terminal

Create an interactive shell session as an authorized target user.

### Administrative terminal

A shell/session capable of privileged system changes.

Each has a different authority level.

## Initial Linux implementation

Existing authenticated SSH is the preferred first transport.

```text
browser/TUI controller
        │
Relmote terminal session
        │
policy + identity
        │
SSH
        │
target PTY
```

Relmote should not require inventing another shell protocol before the UX/policy model is validated.

## Browser terminal

Desired web experience:

```text
TERMINAL — target-host

$ _

Session:
  user
  interactive
  not privileged

[ End terminal ]
```

The browser terminal must be backed by an authenticated Relmote session; merely knowing the web URL must not imply shell authority.

## Permissions

Example policy:

```text
terminal.open          ask
terminal.workspace     allow
terminal.general       ask
terminal.admin         deny
```

## Local visibility

The target TUI/web UI should show active remote terminals and allow the local user to terminate them.

## Audit

Record:

- terminal session start/end;
- controller identity;
- target identity;
- authority/grant;
- approval decisions.

Do not make command-history capture mandatory. Privacy/retention policy should be explicit.

## Future transports

Terminal semantics may later run over:

- native Relmote executor;
- serial console;
- container/VM console;
- hardware Relmote;
- constrained links.

SSH is a transport, not the terminal permission model.
