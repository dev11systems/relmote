# External agent / Codex use case

> Current implementation status lives in [STATUS.md](STATUS.md). The canonical Agent architecture is split between [AGENT-BRIDGE.md](AGENT-BRIDGE.md) and [AGENT-HOST.md](AGENT-HOST.md).

## Goal

Run Codex or another agent away from the target while keeping target authority local, scoped, visible, and revocable.

A current reference topology is:

```text
Browser / CLI               Agent Host                    Relmote Target
   Controller      ───►   Codex / agent adapter   ───►    scoped grant
 approvals/revoke          paired-target service          local enforcement
```

The target does not need Codex installed and does not need to store Codex credentials.

## Why Relmote instead of simply giving the agent SSH

Plain SSH may be perfectly appropriate for a human administrator. Relmote's value for an agent is the smaller, explicit authority envelope:

- approved target identity;
- approved workspace root;
- separate list/read/execute/write capabilities;
- command/tool policy;
- visible session state;
- one-time pairing;
- immediate revocation;
- observations/evidence returned through a structured interface.

The underlying implementation may still use SSH or another transport where appropriate, but transport access does not become the authorization model.

## Current Agent Bridge direction

The target-side Agent API is agent-neutral. A paired Agent Host receives only the capabilities granted by the target.

Initial operations include:

- list within an approved workspace;
- read within an approved workspace;
- run allowlisted commands within an approved workspace;
- inspect session/target state.

Write access, screen observation, and screen control are separate future/experimental grants rather than implied capabilities.

## Pairing

The Controller enables private Agent Access, creates/approves a scoped target grant, and generates a short-lived single-use pairing code. The Agent Host exchanges that code for the session credential over the private Agent endpoint.

After pairing, the human should normally refer to the target by profile/name rather than manually handling URLs or bearer credentials.

## Codex adapter

The planned Codex integration lives on the Agent Host, not the target. MCP is a candidate adapter boundary because it can expose Relmote operations as tools while leaving target authorization in Relmote.

Conceptual tools include: relmote_targets, relmote_target_status, relmote_list, relmote_read, and relmote_exec. Later tools such as write or screen control must exist only when the target grant includes those capabilities.

## Example

Task: diagnose why an application fails to start.

An Agent Host may use the target grant to inspect project files, run approved diagnostics, inspect returned stdout/stderr, and propose a change. If writing is not granted, it must stop at proposal/diagnosis rather than silently modifying the target.

## Validation topology

The first real multi-machine validation should exercise the three roles independently where practical:

1. a human-facing Controller;
2. an Agent Host running the paired-target client/tooling;
3. a Relmote Target enforcing the scoped grant.

Specific hostnames, device brands, and maintainer lab machines are validation details rather than part of the public architecture. Useful test reports should record relevant platform facts such as operating system, architecture, transport, and Relmote build/commit without making a personal lab topology canonical.