# Linux Software Preview

Linux is the reference platform for the first real-world Relmote test.

## Current contributor/tester path

From a checked-out Relmote repository:

```text
./scripts/preview-linux.sh
```

The launcher:

1. checks for Python 3;
2. creates an isolated `.relmote-preview-venv` inside the repo;
3. installs Relmote there;
4. starts the browser preview;
5. does **not** install an OS service.

For trusted-LAN preview:

```text
./scripts/preview-linux.sh --lan
```

For Tailscale, prefer keeping Relmote on localhost and exposing it through the user's existing Tailscale configuration/Serve.

## Current limitation

This still requires obtaining the repository.

The next packaging step is a downloadable Linux artifact that removes Git/source checkout from the tester workflow.

## Desired downloadable preview

```text
Download Relmote
→ mark/run package if required
→ Relmote opens
```

Candidates to evaluate:

- self-contained Python zip/app bundle;
- PyInstaller-style binary;
- AppImage;
- distro packages later.

Do not choose a packaging technology merely because it is fashionable; test:

- launch reliability;
- size;
- update story;
- reproducibility;
- signature/provenance;
- compatibility across target distributions;
- accessibility of logs/uninstall.

## Persistent installation

Not part of the first preview.

Later:

```text
Install Relmote Agent
→ systemd/OpenRC/etc. integration as appropriate
→ stable node identity
→ support normally dormant/on-demand
```

Do not require systemd for core Linux compatibility.
