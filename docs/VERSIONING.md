# Versioning

Relmote uses separate identifiers for human-facing release progression and exact source identity.

## Development snapshots

Example:

```text
Relmote 0.1.0-dev.2 (build d5348540)
```

- `0.1.0` — release series being developed;
- `dev.2` — sequential testable development snapshot;
- `d5348540` — exact source/build identifier.

The development revision advances for **testable snapshots**, not every internal commit.

This keeps ordinary testing understandable:

```text
0.1.0-dev.1
0.1.0-dev.2
0.1.0-dev.3
...
0.1.0-beta.1
0.1.0-rc.1
0.1.0
```

## Package metadata

Python packaging may use a PEP 440-compatible internal version such as:

```text
0.1.0.dev0
```

That package metadata is not required to be the primary human-facing version.

## Exact builds

The short source commit remains visible because two builds with the same development snapshot label should still be distinguishable during debugging.

Full source identity remains available through:

```text
relmote version --full
```

## Revision policy

Increment `DEV_REVISION` when a coherent snapshot is ready for real-world testing.

Do not increment it for every documentation typo or intermediate implementation commit.

Stable releases use ordinary semantic versions and do not display a development revision.
