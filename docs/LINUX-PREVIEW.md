# Linux Software Preview

Linux is Relmote's current reference platform for real-machine software validation.

Current feature availability is tracked in [STATUS.md](STATUS.md). This document covers Linux-specific preview operation rather than serving as the global project status page.

## Recommended repository preview install

Use `pipx` to keep the development preview isolated from the system Python environment:

```bash
pipx install 'relmote[screen-linux] @ git+https://github.com/dev11systems/relmote.git'
relmote
```

Update an existing repository preview with:

```bash
relmote update
```

Verify the human-readable snapshot and exact source build:

```bash
relmote version
```

See [INSTALL-FROM-REPO.md](INSTALL-FROM-REPO.md), [UPDATES.md](UPDATES.md), and [VERSIONING.md](VERSIONING.md).

## Exposure model

Relmote should remain loopback-only unless the user explicitly chooses another exposure path.

For private remote access, the current preferred direction is to keep the underlying service on localhost and use an explicit private transport such as Tailscale Serve. Public Funnel-style exposure is not the default Agent/remote-support model.

The browser controller may use temporary controller authentication while pairing/session UX continues to mature.

## Contributor launcher

A repository checkout may still use the development launcher where useful:

```text
./scripts/preview-linux.sh
```

This is a contributor/testing path, not the primary end-user preview installation.

## Packaging direction

The current repository preview is not a stable distro-native release. Future packaging may include standalone artifacts and OS-native packages/services after update, provenance, compatibility, and uninstall behavior are validated.

Do not require systemd for core Linux compatibility.

## Persistent installation

A mature persistent service remains future work. It should provide stable identity, conservative updates, dormant/on-demand support behavior, and the same capability/session model as the ephemeral preview.