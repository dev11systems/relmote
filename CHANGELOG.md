# Changelog

Notable user-visible changes to Relmote are recorded here.

Relmote is currently in active development. Development snapshot numbers identify coherent testable previews; exact source builds are identified by commit.

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
