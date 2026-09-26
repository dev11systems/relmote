# Cousin workspace test

This is a consented, low-risk real-world test of remote Relmote execution.

## Goal

Prove that a planner/controller on another machine can inspect and propose changes to one explicitly chosen test workspace without installing the planner on the target.

## Setup

Target:

- cousin-owned computer;
- authorized Tailscale + SSH;
- one disposable/test Git repository;
- no secrets in repository;
- no production data.

Controller:

- Rae's machine or another trusted planner host;
- Relmote source/preview;
- existing SSH authentication.

## Phase A — Inspect

Run:

```text
relmote ssh probe <target> hostname
relmote ssh probe <target> uptime
relmote workspace <target> <absolute-root> list
relmote workspace <target> <absolute-root> git-status
relmote workspace <target> <absolute-root> read README.md
```

Verify:

- paths outside root are rejected;
- symlink escape is rejected;
- SSH host identity is expected;
- no target file changes occur.

## Phase B — Proposal

Use the WorkspaceService/API in development to:

1. read one harmless text file;
2. create a proposed replacement;
3. display unified diff;
4. approve explicitly;
5. apply;
6. re-read;
7. verify after-hash.

Use a disposable branch/repository.

## Phase C — Test execution

After explicit approval, run an allowlisted project test.

Treat test/build execution as potentially side-effecting within the workspace.

Do not call it read-only.

## Phase D — Planner bridge

Place Codex or another planner on the controller side.

Initially give it only:

- list;
- read;
- git status/diff;
- propose file change.

Human approves every write and every tool execution.

## Stop conditions

Stop the test if:

- target identity is unexpected;
- root confinement fails;
- a command requests sudo;
- private/home data appears unexpectedly;
- SSH host-key verification changes;
- Relmote attempts an unapproved write.

## Evidence to record

- target OS;
- Relmote commit;
- SSH/Tailscale path;
- configured workspace root;
- operations attempted;
- denied operations;
- proposal diff;
- before/after hashes;
- test results;
- UX confusion.

Do not include secrets or private target content in the public repo.
