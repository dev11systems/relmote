# Workspace Policy v0.1 — Draft

Workspace mode is the bridge for coding agents that run somewhere other than the target.

It grants more than Inspect, but less than a general SSH account.

## Policy object

Conceptual example:

```yaml
target: cousin-host
roots:
  - path: /home/user/project
    read: true
    write: true

tools:
  - git
  - python
  - pytest
  - npm

network:
  outbound: ask

system:
  package_install: ask
  service_change: ask
  sudo: deny
```

## Filesystem

Every file operation is resolved against configured roots.

Reject:

- path traversal outside root;
- symlink escape where detectable;
- implicit home-directory access;
- SSH/private credential directories unless explicitly granted.

## Commands

Do not expose arbitrary shell strings as the core API.

Prefer structured execution:

```text
tool: git
args: [status, --short]
cwd: /configured/root
```

The executor validates:

- tool is allowed;
- cwd is inside an allowed root;
- environment additions are allowed;
- timeout/resource limits.

## Shell

A general shell may eventually exist as an explicit high-authority capability.

It is not required for Workspace MVP.

## Writes

File writes should record:

- path;
- before/after digest where practical;
- task/action ID;
- controller/planner;
- result.

Git workspaces provide an especially useful additional audit/revert layer but are not mandatory.

## Secrets

Default-deny likely secret locations and environment values.

Planner-visible environment should be constructed deliberately rather than inheriting every target process secret.

## System changes

Workspace mode does not imply:

- sudo;
- package install;
- service restart;
- firewall changes;
- OS configuration.

Those belong to Support/System capabilities.

## Purpose

The goal is not to make SSH weaker for humans.

The goal is to give automated planners a smaller, legible authority envelope than the human SSH account underneath.
