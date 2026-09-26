# Codex / external agent bridge

Relmote should allow an AI/coding agent to live **somewhere other than the target machine**.

The target should not need the full agent UI/CLI merely so an authorized planner can work with it.

## Pattern A — remote planner + SSH target

Best immediate path when SSH already exists.

```text
Codex host
  Rae laptop/server
       │
       │ planner proposes work
       ▼
Relmote controller/bridge
       │
       │ Tailscale + SSH
       ▼
cousin computer
```

Codex runs on the trusted planner machine.

Relmote exposes the target as capabilities such as:

```text
shell.read
shell.write
file.read
file.write
process.inspect
service.inspect
```

subject to target/controller policy.

### Important boundary

Do not simply hand an autonomous planner an unrestricted SSH private key and call that Relmote.

Relmote should mediate:

- target identity;
- allowed working roots;
- read/write capability;
- command approval;
- task/session expiry;
- evidence/results;
- revoke.

For the earliest prototype, an existing SSH account plus manual approvals is acceptable.

## Pattern B — small target executor

A target may run a small Relmote executor rather than a full controller/planner.

```text
Codex / planner host
        │
        ▼
Relmote protocol
        │
        ▼
small Relmote executor
on target
```

The executor exposes only configured capabilities.

This resembles agent systems where a remote harness delegates execution into a self-hosted environment.

Advantages:

- no full AI stack on target;
- outbound-only connectivity is possible;
- structured capability boundary;
- richer than raw SSH;
- easy temporary deployment.

## Pattern C — OpenAI self-hosted agent environment

OpenAI's Agents API supports self-hosted environments using a `codex exec-server` running inside the environment.

The OpenAI agent harness remains remote while the executor:

- reads/writes files;
- runs shell commands;
- accesses local MCP servers;
- connects outbound over WebSocket.

This can be useful where installing a small OpenAI executor is acceptable.

It is distinct from Relmote and should remain an optional integration rather than a platform dependency.

## Pattern D — hardware Relmote

If the target cannot run SSH or an executor:

```text
Codex host
    │
 Relmote task/proposals
    │
Pocket
    │
HID / KVM / serial
    │
target
```

This is the physical fallback.

## Planner location

A Codex-like planner might live on:

- Rae's laptop;
- home server;
- VM;
- cloud development environment;
- future Relmote planner service.

The target need only expose an authorized execution path.

## Working-root policy

For coding tasks, a Relmote SSH/executor target should allow explicit roots:

```text
/home/user/project-a       read/write
/etc                       read only
/home/user/private         unavailable
```

Do not treat SSH account access as justification for exposing the entire account filesystem to every planner task.

## Command policy

Initial useful modes:

### Inspect

- read files;
- inspect Git;
- run safe diagnostic commands;
- no writes.

### Workspace

- read/write configured project roots;
- run project build/tests;
- no system administration.

### Support

- inspect system;
- propose administrative commands;
- require explicit approval for changes.

### Infrastructure

Owner-configured automation for a dedicated target.

## Credentials

Preferred progression:

1. existing SSH authentication owned by the human/controller;
2. dedicated constrained SSH key/account;
3. Relmote executor with its own scoped identity;
4. richer pairing/capability protocol.

Avoid copying long-lived personal private keys into AI prompts or model context.

## Design principle

> **The planner does not need to live where execution happens.**

Relmote's job is to make the remote execution boundary explicit, inspectable, revocable, and transport-independent.
