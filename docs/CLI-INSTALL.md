# CLI installation

CLI installation is a first-class Relmote distribution path.

## Desired ordinary-user path

Eventually, after the installer and release pipeline are validated:

```bash
curl -fsSL <official Relmote installer URL> | sh
```

The command shown on the project site must point to a stable, reviewable installer owned by the Relmote project.

## Safer inspect-first path

Users should also be encouraged/able to:

```bash
curl -fsSL <installer URL> -o install-relmote.sh
less install-relmote.sh
sh install-relmote.sh
```

Convenience must not require opacity.

## What the installer does

The Linux preview installer:

1. detects Linux architecture;
2. selects the matching release artifact;
3. downloads the binary over HTTPS;
4. downloads published SHA-256 checksums;
5. verifies the selected artifact;
6. installs as `~/.local/bin/relmote` by default;
7. prints version/build information.

It does **not**:

- install a system service;
- enable support;
- open a network listener;
- create an account;
- modify SSH/Tailscale;
- require root.

## Custom location

```bash
RELMOTE_INSTALL_DIR=/some/path sh install.sh
```

Default:

```text
~/.local/bin/relmote
```

## Version pinning

The installer supports a specific release:

```bash
RELMOTE_VERSION=preview-0.1 sh install.sh
```

This matters for reproducibility and support.

## Updating

Near-term:

```text
relmote update
```

should eventually:

- check the configured release channel;
- show current/new version;
- download and verify;
- ask before replacing the executable.

Until that exists, rerunning the installer is acceptable.

## Uninstall

Portable CLI installation should remain boring:

```bash
rm ~/.local/bin/relmote
```

Persistent Agent packages will need a separate uninstall path because they own service/config/state files.

## Distro-native future

The preferred installed experience can later include:

```bash
apt install relmote
dnf install relmote
```

and community packaging for other distributions.

The universal installer remains useful for previews and distributions without a native package.

## Trust improvements before public recommendation

Before advertising pipe-to-shell installation broadly:

- validate the release artifact on real systems;
- publish checksums;
- add release provenance/signing;
- pin installer/release behavior carefully;
- document what persistent state exists;
- provide inspect-first instructions beside the one-liner.
