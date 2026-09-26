# Software deployment

Relmote software should support a spectrum from **temporary run** to **installed service**.

## Tier 0 — source/development

For contributors:

```bash
git clone ...
python -m venv .venv
. .venv/bin/activate
pip install -e .
relmote serve
```

## Tier 1 — ephemeral Python environment

Where Python tooling is already available, use an isolated runner/environment so Relmote does not need to become a permanent system service.

Desired experience:

```text
run Relmote
→ localhost browser UI
→ support/diagnostics
→ stop process
→ environment can be discarded
```

## Tier 2 — standalone executable

Build signed/reproducible platform executables for:

- Windows;
- macOS;
- Linux.

Desired:

```text
Relmote.exe
Relmote.app / relmote
relmote-linux
```

The executable should default to temporary localhost mode.

## Tier 3 — installed Agent

Explicit user action installs `relmoted` as an OS service.

This enables:

- stable node identity;
- persistent pairing;
- unattended/infrastructure modes if configured;
- startup on boot.

Installing the service must not silently enable remote access.

## Tier 4 — OS packages

Potential later packaging:

- deb/rpm;
- Homebrew;
- Windows package;
- other community packages.

Package-manager presence does not change the security model.

## Browser behavior

Relmote may optionally open the localhost controller automatically after launch.

Do not open a public/LAN listener merely to make mobile access easier.

## Portable state

Temporary mode should keep persistent state minimal.

Candidate choices:

- ephemeral node identity by default;
- explicit “remember this node” action to persist identity;
- temporary sessions;
- no unattended access.

## Installed state

Installed mode needs a protected state directory containing:

- node identity;
- paired controllers;
- owner policy;
- audit/task metadata;
- settings.

Exact OS paths will be platform-specific and documented.

## Updates

Relmote should eventually support:

- signed releases;
- reproducible/build provenance where practical;
- explicit release notes;
- no forced cloud account;
- owner-controlled update policy for infrastructure nodes.
