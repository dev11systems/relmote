# Agent Host baseline validation — 2026-09-26

**Result: PASS**

This record captures a real-machine validation of the Relmote Controller → Agent Host → Target path. It is intentionally redacted for public documentation.

No personal hostnames, usernames, private network addresses, pairing codes, bearer credentials, or private tailnet details are included.

## Environment

| Field | Observed value |
| --- | --- |
| Date | 2026-09-26 |
| Controller | browser on tablet |
| Agent Host | Linux / x86_64 |
| Target | Linux / x86_64 |
| Target Relmote build | `8770f5acdf483aba32e21761af04b2c961265e8d` |
| Agent Host final Relmote build | `889406798af495df332e3e6bdefed9f84fa7a5b7` |
| Package channel | repository preview |
| Private transport | direct Tailscale IPv4 interface bind |
| Workspace | disposable Git test directory |
| Initial capabilities | `workspace.list`, `workspace.read` |
| Expanded capabilities | `workspace.list`, `workspace.read`, `terminal.exec` |

The Controller, Agent Host, and Target were separate roles. The Agent Host and Target were separate machines.

## Observed results

### Transport

- Enabling Agent Access started the Agent API on the Target's exact Tailscale address rather than a wildcard bind.
- Tailscale Serve was not required.
- An unauthenticated browser request reached the Agent API but was rejected because an Agent bearer credential was required.
- Disabling Agent Access removed network reachability to the Agent API; the Agent Host received a connection-refused/unavailable result.
- Re-enabling transport restored reachability but did not restore the old Agent session authority.

### Pairing

- A short-lived pairing code successfully paired the Agent Host once.
- The Agent Host stored a local paired-target profile without printing the bearer credential.
- Reusing the already consumed pairing code was rejected.
- Repeating the reuse attempt remained rejected.

### Read-only workspace capability

With only `workspace.list` and `workspace.read` granted:

- paired-target status succeeded;
- listing the approved workspace succeeded;
- reading a harmless file in the approved workspace succeeded;
- listing `..` was rejected because it escaped the configured workspace root;
- reading a file through `../` was rejected for the same reason;
- `terminal.exec` was rejected because it had not been granted.

### Explicit execution capability

A new narrow grant was created for the same disposable workspace with `terminal.exec` explicitly added.

- the Agent Host paired to the new grant;
- target/session status showed the expanded capability set;
- allowlisted `git status` executed successfully inside the approved workspace.

This demonstrated both sides of the capability boundary: execution was denied before the grant and succeeded after explicit authorization.

### Revocation

The original paired Agent session was revoked on the Target while private transport remained reachable.

- the stored Agent Host credential remained present locally;
- status using that credential was rejected because the Agent session was no longer active;
- workspace listing using that credential was also rejected.

Connectivity therefore did not preserve authority after target-side revocation.

### Transport shutdown and restore

With an active explicitly authorized execution grant:

1. Agent Access was disabled on the Target.
2. The Agent Host could no longer reach the Agent API.
3. Agent Access was re-enabled without creating a new grant.
4. The previous Agent Host credential reached the API again but was rejected because its Agent session was no longer active.

This confirms that transport availability and Agent authority are independent state.

## Baseline criteria

- [x] exact build identities recorded;
- [x] Agent Host capability discovery works;
- [x] one-time pairing succeeds once;
- [x] consumed pairing code is rejected;
- [x] paired target is addressable by profile name;
- [x] status works;
- [x] workspace list works;
- [x] workspace read works;
- [x] workspace confinement remains enforced;
- [x] allowlisted execution works only when separately granted;
- [x] revocation invalidates the previously paired credential;
- [x] transport shutdown removes remote Agent API reachability;
- [x] restoring transport does not restore revoked authority;
- [x] no bearer credential appears in normal CLI output;
- [x] no unapproved authority appeared during the test.

## Remaining follow-up

This PASS validates the current Linux/x86_64 direct-Tailscale baseline. It does not establish:

- cross-platform parity;
- production credential/keyring storage;
- arbitrary command execution;
- write capability;
- screen observation/control;
- Hub/rendezvous behavior;
- behavior across every Tailscale ACL/sharing topology.

Those remain separate implementation and validation milestones.
