# External agent use case

## Remote coding/support without installing the planner on the target

Scenario:

- target is an authorized computer;
- target is already reachable through Tailscale;
- SSH is available;
- an authorized user wants Codex or another planner to run elsewhere.

```text
Controller / Codex host
       │
       │ Tailscale
       ▼
Relmote SSH adapter
       │
       ▼
remote target
```

The target can remain free of Codex itself.

Relmote should surface:

- target identity;
- SSH host identity;
- configured workspace roots;
- available commands/capabilities;
- requested changes;
- actual stdout/stderr as observations.

## Example

Task:

```text
Diagnose why this application fails to start.
```

Planner may request:

1. inspect project files;
2. inspect service/log state;
3. run read-only diagnostics;
4. propose a patch;
5. request permission to write the patch;
6. run tests.

Relmote records which observations support the result.

## Why not just SSH?

For a human, plain SSH may be sufficient.

Relmote becomes useful when an agent is involved because it can impose a smaller authority envelope than the underlying SSH account and preserve task/evidence/approval semantics.

SSH is then the transport, not the policy model.
