# Changelog

Notable user-visible changes to Relmote are recorded here.

Relmote is currently in active development. Development snapshot numbers identify coherent testable previews; exact source builds are identified by commit.

## 0.1.0-dev.12 — 2026-09-26

Validated cross-machine Agent Host baseline.

### Agent Access and Agent Host

- Switched the baseline private Agent transport from Tailscale Serve to a direct bind on the target's exact Tailscale IPv4 address.
- Kept Tailscale Serve/HTTPS optional rather than requiring tailnet-admin setup or public certificate issuance.
- Added Agent Host capability discovery and locally stored paired-target profiles.
- Added paired-target status, workspace list/read, and allowlisted execution.
- Added short-lived, single-use pairing codes for Agent Host enrollment.
- Preserved target-side authority after pairing: revoked sessions reject already-paired Agent Host credentials.
- Validated workspace traversal confinement and denial of ungranted execution.
- Validated explicit execution escalation: allowlisted execution succeeds only after a new grant includes `terminal.exec`.
- Validated transport shutdown and restore independently from authority: disabling Agent Access removes reachability, while re-enabling transport does not restore revoked grants.
- Recorded a redacted real-machine PASS in `docs/validation/AGENT-HOST-BASELINE-2026-09-26.md`.

### Private transport and trust

- Added exact-interface direct Tailscale Agent API binding; wildcard `0.0.0.0` is not used as a substitute.
- Added an explicit rule against silently creating public metadata side effects such as publicly logged TLS certificate names.
- Documented shared-machine/private-tailnet topologies where direct Tailscale reachability works but Serve administration may not.
- Added the future Hub/rendezvous direction without making the Hub the root of trust.

### Debugging and UX

- Added persistent rotating per-user debug logs.
- Added `relmote logs`, `relmote logs --path`, and file export through `relmote logs --save`.
- Converted expected authorization denials from Python tracebacks into concise `Denied:` messages.
- Converted unreachable Agent endpoints into concise `Unavailable:` messages.
- Fixed Agent Access lifecycle requests to use the correct HTTP method.
- Clear stale pairing-code UI when Agent Access is disabled/off.

### Hub direction

- Defined the optional self-hosted Relmote Hub role.
- Made Hub + Agent Host co-location a first-class deployment while keeping credentials and authority logically separate.
- Scoped the first Hub MVP around inventory, version coordination, session overview, and rendezvous before optional relay.

### Snapshot note

Development snapshots dev.4 through dev.11 were iterative repository previews. Their individual changes are not being retroactively reconstructed here; dev.12 is the next normalized changelog checkpoint.

## 0.1.0-dev.3 — in development

### Web and UX

- Reworked the web preview toward Overview, Diagnostics, Terminal, Help, and Activity sections.
- Added clearer mobile/tablet navigation and touch targets.
- Made long evidence and terminal output independently scrollable.
- Clarified that capability labels describe available abilities rather than acting as buttons.
- Added visible action/error feedback instead of silent web failures.
- Updated remote-access help/copy to reflect implemented private Tailscale binding.

### Terminal

- Made terminal approval transactional.
- Added visible terminal startup/PTY errors.
- Preserved separate normal-user and administrative authority; administrative terminal remains unavailable in the preview.

### Diagnostics

- Added readable summaries for System, Network, and Storage focused checks.
- Expanded Full Check with more system detail while preserving explicit uncertainty/not-tested states.

## 0.1.0-dev.2

First coherent real-machine Fedora/Tailscale web preview.

- Repository install/update workflow via pipx.
- Sequential development snapshot versioning groundwork.
- Linux doctor and Full Check.
- CLI/TUI/web shared runtime.
- Automatic Tailscale-only web binding when Tailscale is connected.
- Localhost fallback; no automatic 0.0.0.0 exposure.
- Per-run token for non-local preview access.
- Remote-support availability policy.
- Initial browser terminal request/PTY prototype.
- Safari web-script escaping fix.
- Shared plain-language help.
- SSH/workspace foundations.

## Earlier prototype work

Earlier commits established:

- Relmote software/hardware architecture;
- Linux reference adapter;
- evidence-oriented diagnostics;
- support/session policy;
- SSH target probes;
- workspace confinement and proposal foundations;
- packaging and standalone Linux artifact CI;
- screen/terminal capability architecture.

These were exploratory development commits before sequential test snapshots were introduced.

