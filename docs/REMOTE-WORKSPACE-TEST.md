# Remote workspace test

This is a consented, low-risk test of remote Relmote execution.

## Goal

Prove that a planner/controller on another machine can inspect and propose changes to one explicitly chosen test workspace without requiring the planner itself on the target.

## Setup

Target:

- authorized test computer;
- authenticated private-network + SSH path or equivalent;
- disposable/test Git repository;
- no secrets or production data in the test workspace.

Controller:

- trusted controller/planner host;
- Relmote preview;
- existing authenticated transport.

## Phase A — Inspect

Run:

```text
relmote ssh probe <target> hostname
relmote ssh probe <target> uptime
relmote workspace <target> <absolute-root> list
relmote workspace <target> <absolute-root> git-status
relmote workspace <target> <absolute-root> read README.md
```

Verify path traversal and symlink escapes are rejected and no target files change.

## Phase B — Proposal

Use the WorkspaceService/API to read a harmless text file, propose a replacement, display a unified diff, explicitly approve it, apply it, re-read it, and verify the resulting digest.

## Phase C — Tool execution

After explicit approval, run an allowlisted project test. Treat test/build execution as potentially side-effecting within the workspace.

## Phase D — Planner bridge

Place an external planner on the controller side. Initially grant only list, read, Git status/diff, and propose-file-change operations. Human approval remains required for writes and tool execution.

## Stop conditions

Stop if target identity is unexpected, root confinement fails, an unexpected privilege request occurs, unrelated private data appears, host authentication changes unexpectedly, or an unapproved write is attempted.

Do not include secrets or private target content in public test reports.
