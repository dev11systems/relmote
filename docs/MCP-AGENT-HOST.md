# MCP / Codex Agent Host adapter

Relmote's first MCP adapter exposes the already-validated paired-target service to a local MCP host such as Codex.

The adapter does not create a second authorization model.

```text
Codex
  │ local MCP over stdio
  ▼
relmote-mcp
  │
  ▼
PairedTargetService
  │ stored profile credential stays internal
  ▼
Relmote Agent API
  │
  ▼
Target-side workspace + capability policy
```

## Installation

MCP is optional so ordinary Relmote Targets do not need the MCP SDK.

Install the Agent Host with the MCP extra:

```bash
pipx install --force 'relmote[mcp] @ git+https://github.com/dev11systems/relmote.git@main'
```

On a host that also needs the Linux screen optional dependency:

```bash
pipx install --force 'relmote[screen-linux,mcp] @ git+https://github.com/dev11systems/relmote.git@main'
```

The official MCP Python SDK v2 is the supported line for this adapter.

## Server

The installed local MCP command is:

```bash
relmote-mcp
```

It uses stdio by default. Stdout is reserved for the MCP protocol.

## Role semantics

The MCP server sends explicit server-level instructions to the MCP host:

- Codex is running on the **Agent Host**.
- A `target` argument names a separately paired **Target**.
- Target workspace paths are not Agent Host filesystem paths.
- `relmote_list`, `relmote_read`, and `relmote_exec` operate on the named Target.
- A Relmote denial must not be treated as permission to bypass Relmote using local shell, SSH, Tailscale, or another path.

Every Target operation also returns structured context naming the Target role and execution/path location. The adapter does not depend on the model remembering a single prose instruction.

## Initial tools

### `relmote_context`

Returns the Agent Host vs Target role model and authority/bypass rules without exposing credentials or local filesystem contents.

### `relmote_targets`

Returns credential-blind summaries of locally paired targets.

It does not expose:

- bearer credentials;
- stored Agent API endpoint URLs;
- raw profile JSON.

### `relmote_target_status`

Fetches live status using the paired target's stored credential.

A revoked session remains revoked; MCP cannot revive it.

### `relmote_list`

Lists a path inside the target-authorized workspace.

Target-side workspace confinement remains authoritative.

### `relmote_read`

Reads a text file inside the target-authorized workspace.

### `relmote_exec`

Requires the target to grant `terminal.exec`.

The first MCP adapter intentionally exposes named operations rather than arbitrary command vectors:

- `git_status` → `git status`;
- `git_diff` → `git diff`;
- `pytest` → `pytest` with explicit pytest arguments.

This is narrower than the raw paired-target service by design.

Expected target-side policy and reachability failures are returned as structured results rather than opaque MCP server errors:

```text
ok: false
error:
  kind: denied | unavailable | invalid_request
  message: <target/transport reason>
```

This lets the MCP host distinguish an authorization denial from transport loss or an invalid target request without exposing credentials.

## Codex connection

Codex supports MCP servers in both the CLI and IDE extension, with shared configuration.

After installing the MCP extra on the Agent Host, add the local server to Codex using its MCP configuration/CLI, with `relmote-mcp` as the stdio command.

Verify the configured servers with:

```bash
codex mcp list
```

The exact Codex CLI syntax should follow the installed Codex version. The validation goal is that Codex discovers the six Relmote MCP tools above and receives the Agent Host/Target role instructions before operating on a Target.

## Authority validation

The first real Codex test should repeat the already-validated CLI boundary:

1. Codex reads `relmote_context` and correctly describes itself as running on an Agent Host while the paired machine is a separate Target.
2. Codex discovers the paired target.
3. With a read-only target grant, Codex can list/read only the approved workspace.
4. Codex reports those paths as Target paths rather than Agent Host paths.
5. Codex cannot execute when `terminal.exec` is absent.
6. Codex does not attempt to bypass that denial using another transport.
7. With a fresh explicit exec grant, `git_status` succeeds on the Target.
8. Revoke the target grant.
9. A subsequent Codex tool call fails.
10. Disabling Agent Access removes target reachability.

Do not promote the MCP/Codex adapter to exercised status until this is observed on a real Agent Host.
