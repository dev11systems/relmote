# SSH target adapter

The first external-target implementation uses the user's existing OpenSSH client.

## Why

For an authorized private-network preview, Tailscale + SSH can provide:

- encrypted transport;
- host authentication;
- user authentication;
- remote command execution.

Relmote should add capability/task/evidence policy above that instead of rebuilding SSH.

## Preview mode: Inspect

The first adapter exposes **named read-only probes**, not arbitrary shell input.

Current prototype probes include:

- identity;
- hostname;
- uptime;
- disk;
- Linux memory;
- Linux addresses;
- Linux routes.

Example:

```text
relmote ssh target-host probe hostname
```

The result becomes a Relmote observation.

## SSH configuration

Relmote uses the host `ssh` executable.

Therefore normal user configuration can provide:

- Tailscale hostname/IP;
- SSH keys;
- host-key checking;
- ProxyJump;
- custom usernames;
- hardware-backed keys.

Relmote should not ingest private SSH key material into planner prompts.

## Batch mode

Preview probes use OpenSSH BatchMode.

If authentication requires an interactive password/prompt, the probe fails rather than hanging a background agent.

Users can establish suitable SSH authentication separately.

## Future Workspace mode

A coding-agent bridge will add a workspace-scoped executor with explicit roots.

Example:

```yaml
target: target-host
roots:
  ~/project:
    read: true
    write: true
commands:
  - git
  - pytest
  - npm
system_write: false
```

This should be a separate capability from Inspect.

## Future Support mode

System-changing commands are proposed as structured actions and require policy/approval.

Do not turn `SSHTarget` into `subprocess.run(user_supplied_string, shell=True)`.
