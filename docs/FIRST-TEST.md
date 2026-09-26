# First Relmote test

This is the baseline workflow for early Linux testers.

## Install from the repository

    pipx install 'git+https://github.com/dev11systems/relmote.git'

## Verify the machine

    relmote doctor

Required checks should pass.

Optional SSH/Tailscale/systemd tooling may be absent without preventing local Relmote use.

## Check the build

    relmote version

Record this when reporting a bug.

## Launch

    relmote

Expected:

- terminal/TUI starts;
- localhost web runtime starts;
- no remote support is silently enabled.

## First operations

1. Check this computer.
2. Run network diagnosis.
3. Open the web interface locally.
4. Confirm TUI and web show the same tasks/state.
5. Quit Relmote.
6. Confirm no persistent Relmote service remains.

## Update during development

After a new tested feature lands:

    relmote update

Restart Relmote.

## Report useful failures

Capture:

- relmote version
- relmote doctor
- Linux distribution/version
- what you attempted
- what happened
- what you expected

Do not include secrets, private SSH material, or unrelated personal files.

## Remote/Tailscale test

Only after local operation is confirmed.

Use the existing authorized private-network setup and follow the current Tailscale/SSH preview docs.

## Status

This is an experimental development preview.

It is suitable for consented testing on noncritical systems/workspaces, not yet a production remote-management deployment.
