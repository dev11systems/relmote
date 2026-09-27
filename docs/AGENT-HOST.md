# Relmote Agent Host

An Agent Host supplies compute and agent tooling for one or more authorized Relmote targets.

Controller, Agent Host, and Target are independent roles.

Example deployment: a browser on a phone, tablet, or computer serves as the Controller; a workstation, server, or VM serves as the Agent Host; and an authorized computer serves as the Target. Moving the Agent Host to another machine does not change target-side authorization.

## Responsibilities

- Pair with targets using short-lived one-time codes.
- Retain paired target profiles using local credential storage.
- Expose authorized target capabilities to an agent.
- Run agent tooling such as Codex.
- Report host capabilities to a future Relmote Hub.

An Agent Host does not create target authority. Every target grant originates from and remains revocable by the target/controller authorization model.

## Current implementation boundary

The current CLI and future adapters share one paired-target service rather than each reimplementing profile and credential handling.

That service exposes the current target operations:

- enumerate paired targets without exposing bearer credentials;
- inspect target/session status;
- list an authorized workspace path;
- read an authorized workspace file;
- execute a target-authorized command.

The CLI and the first local stdio MCP adapter are consumers of this boundary. The MCP adapter is intentionally credential-blind and does not broaden target capabilities.

## Private transport

The baseline Agent Host path uses the target's direct Tailscale address when available. Enabling Agent Access starts a listener bound only to that exact Tailscale address; disabling Agent Access revokes active grants before stopping that listener.

Tailscale Serve is optional HTTPS convenience, not a prerequisite. This avoids making Agent Access depend on tailnet-admin features and allows the same Relmote authorization model to work with shared-in machines when Tailscale reachability permits it.

The Agent Host stores the endpoint in the paired target profile after the one-time pairing exchange.

## Adapter boundary

The target-side Agent API remains agent-neutral. An Agent Host adapter can expose paired targets through MCP or another agent tool protocol.

Initial MCP tools: relmote_targets, relmote_target_status, relmote_list, relmote_read, relmote_exec. See [MCP-AGENT-HOST.md](MCP-AGENT-HOST.md).

Later, when separately authorized: relmote_write, relmote_screen_observe, relmote_screen_control.

Adapters must not broaden target capabilities. A read-only target grant cannot become write authority through the adapter.

## Host selection

The future Relmote Hub may choose among authorized Agent Hosts based on online state, installed tools, compute capacity, locality/latency, privacy policy, workload, and user preference. Automatic selection must remain visible and overridable.

## Credential storage

The preview uses owner-only local profile files. Production design should prefer OS credential/keyring storage and avoid exposing bearer material in command arguments, logs, UI, agent context, or adapter tool results.

## Validation

Before treating the cross-machine Agent Host path as exercised, run the reproducible checks in [AGENT-HOST-VALIDATION.md](AGENT-HOST-VALIDATION.md). CI success alone does not establish the multi-machine authority and revocation behavior.
