# Updates

Relmote should be easy to update during rapid preview development.

## Repository preview

If installed with:

```bash
pipx install 'git+https://github.com/dev11systems/relmote.git'
```

the intended workflow is:

```bash
relmote update
```

The preview implementation refreshes the pipx application from the repository.

Restart a running Relmote process after updating.

## Check without changing anything

```bash
relmote update --check
```

shows the update source/command without mutating the installation.

A future release-aware updater will compare actual available versions before offering an update.

## Development warning

The `main` branch is moving quickly.

For a known test session, pinning a tested commit/tag is safer than updating in the middle of a support operation.

## Future channels

Planned:

- stable;
- preview;
- development.

Users should choose a channel explicitly.

## Persistent state

Program updates should eventually preserve separately stored:

- node identity;
- trusted helpers;
- policy;
- settings;
- audit/history according to retention policy.

The current ephemeral preview has little persistent state yet.

## Safety

Relmote should never silently replace itself during an active support session.

Future automatic update checks may notify, but installation remains explicit unless an owner deliberately configures an update policy.
