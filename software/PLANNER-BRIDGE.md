# Planner bridge

A remote planner such as Codex should interact with a Relmote target through semantic operations.

## Inspect phase

Available now as the first SSH target adapter:

```text
planner/controller
→ Relmote
→ named read-only probe
→ SSH
→ target
→ stdout/stderr observation
```

## Workspace phase

Next implementation:

```text
planner
  │
  ├─ read(path)
  ├─ write(path, content)
  ├─ list(path)
  └─ exec(tool, args, cwd)
       │
       ▼
Relmote Workspace Policy
       │
       ▼
SSH/executor target
```

## Support phase

Later:

```text
planner proposes:
  service.restart("foo")

Relmote:
  policy says ASK

human:
  approves once

executor:
  performs action

observation:
  actual result
```

## Planner independence

The bridge should work with:

- Codex;
- another cloud planner;
- local LLM;
- deterministic automation;
- human-authored task runner.

No planner gets a privileged bypass around Relmote policy.
