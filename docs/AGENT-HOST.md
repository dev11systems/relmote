# Relmote Agent Host

An Agent Host supplies compute and agent tooling for one or more authorized Relmote targets.

Controller, Agent Host, and Target are independent roles.

Example deployment: Controller = iPad web UI; Agent Host = Kaonashi; Target = russ-pc. A later deployment may use Falkor without changing target-side authorization.

## Responsibilities

- Pair with targets using short-lived one-time codes.
- Retain paired target profiles using local credential storage.
- Expose authorized target capabilities to an agent.
- Run agent tooling such as Codex.
- Report host capabilities to a future Relmote Hub.

An Agent Host does not create target authority. Every target grant originates from and remains revocable by the target/controller authorization model.

## Adapter boundary

The target-side Agent API remains agent-neutral. A controller-side adapter can expose paired targets through MCP or another agent tool protocol.

Initial conceptual MCP tools: relmote_targets, relmote_target_status, relmote_list, relmote_read, relmote_exec.

Later, when separately authorized: relmote_write, relmote_screen_observe, relmote_screen_control.

Adapters must not broaden target capabilities. A read-only target grant cannot become write authority through the adapter.

## Host selection

The future Relmote Hub may choose among Agent Hosts such as Kaonashi and Falkor based on online state, installed tools, compute capacity, locality/latency, privacy policy, workload, and user preference. Automatic selection must remain visible and overridable.

## Credential storage

The preview uses owner-only local profile files. Production design should prefer OS credential/keyring storage and avoid exposing bearer material in command arguments, logs, UI, or agent context.