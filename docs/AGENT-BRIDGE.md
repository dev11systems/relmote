# Agent bridge

Relmote can expose an explicitly authorized target as a constrained execution/workspace environment to an agent running elsewhere.

The target does not need the agent runtime installed. For example, Codex may run on a controller, server, or dedicated agent host while Relmote runs on the target.

## Boundary

Relmote is the target-side authority boundary, not the agent.

Initial capabilities should be separate grants:

- `workspace.list`
- `workspace.read`
- `workspace.write`
- `terminal.exec`
- `system.observe`
- later: `screen.observe` and `screen.control`

An agent bridge must not turn remote-support availability into blanket filesystem or shell authority.

## Proposed flow

1. Target user enables remote support.
2. Controller requests an agent session.
3. Target approves a workspace and capabilities.
4. Relmote issues a scoped session.
5. Agent-side adapter maps its operations onto Relmote capabilities.
6. Relmote records operations and enforces scope/revocation.
7. STOP or support-disable immediately invalidates the session.

## Codex

Codex may run away from the target. A Relmote adapter can present target files and command execution to Codex while keeping Codex credentials and installation off the target machine.

The first implementation should use Relmote's existing confined-workspace and terminal primitives. It should not expose the target's entire SSH account merely because SSH transport exists.

Future integrations may include MCP, Codex App Server clients, or self-hosted agent-environment adapters. These are controller-side integrations; the Relmote target protocol should remain agent-neutral.