# Agent Host multi-machine validation

This runbook validates the current Relmote Controller → Agent Host → Target path on authorized systems.

It is a validation procedure, not evidence that the path has already passed. Record results only after they are observed.

A redacted real-machine baseline PASS is recorded in [validation/AGENT-HOST-BASELINE-2026-09-26.md](validation/AGENT-HOST-BASELINE-2026-09-26.md).

## Goal

Prove that:

1. a human-facing Controller creates a narrow target grant;
2. a separate Agent Host pairs to that grant without receiving broader authority;
3. the Agent Host can use only the approved target capabilities;
4. a pairing code cannot be reused;
5. revocation on the target/controller side immediately prevents further Agent Host operations.

The baseline validation should use separate Controller, Agent Host, and Target roles where practical.

## Safety and test data

Use only systems the operator owns or is authorized to administer.

For the first run:

- use a disposable or non-sensitive workspace;
- do not include credentials, private keys, personal documents, or production data;
- begin with list/read capabilities;
- add allowlisted execution only after list/read succeeds;
- do not grant write, administrative, screen-control, or unrelated filesystem access.

Public validation notes must follow [DOCS.md](DOCS.md): record reproducible platform facts, not personal hostnames, private network details, or raw secrets.

## Validation record

Record these facts before testing:

| Field | Value |
| --- | --- |
| Date | |
| Relmote commit | |
| Relmote displayed version/build | |
| Artifact/package source | |
| Artifact SHA-256, if applicable | |
| Controller type | browser / CLI / other |
| Agent Host OS | |
| Agent Host architecture | |
| Target OS | |
| Target architecture | |
| Private transport | direct Tailscale / Tailscale Serve / LAN / other |
| Workspace type | disposable repo / test directory / other |

Use generic labels such as `controller-a`, `agent-host-a`, and `target-a` in notes.

## 1. Preflight

On the Target and Agent Host, confirm the exact build:

```bash
relmote version --full
```

On the Agent Host:

```bash
relmote agent host
```

Confirm that the reported operating system, architecture, and detected tools are reasonable for that host.

**Pass:** build identity is recorded and the Agent Host command completes without exposing credentials.

## 2. Start the Target controller

Start Relmote on the Target using the preview method being tested.

For the baseline Tailscale validation, confirm that the Target has a Tailscale IPv4 address. Direct Tailscale binding is the preferred Agent transport; Tailscale Serve is not required.

Open the human Controller and:

1. enable Remote Support;
2. enable private Agent Access;
3. choose a narrow test workspace;
4. initially grant only workspace list/read capabilities;
5. approve the Agent session;
6. generate a short-lived, single-use pairing code.

Record the private Agent endpoint only in private test notes. Do not commit it to the repository.

## 3. Pair the Agent Host

On the Agent Host:

```bash
relmote agent pair <private-agent-url> --name target-a
```

Enter the pairing code interactively when requested.

Then:

```bash
relmote agent targets
relmote agent use target-a status
```

**Pass:** the paired target appears by profile name, the approved workspace/capabilities are visible, and no bearer credential is printed.

For a direct-Tailscale run, also confirm the pairing endpoint uses the Target's Tailscale address and that Relmote did not bind the Agent API to every interface.

## 4. Exercise read-only workspace operations

List the approved workspace:

```bash
relmote agent use target-a list .
```

Read a harmless text file known to exist within that workspace:

```bash
relmote agent use target-a read README.md
```

Use another harmless path if the test workspace does not contain `README.md`.

**Pass:** in-scope content is returned and no operation can escape the approved workspace.

If practical, also verify that a traversal attempt such as `../` is rejected.

## 5. Verify one-time pairing

Attempt to pair again using the already consumed pairing code.

**Pass:** the second exchange fails. The consumed code must not mint another credential.

Generate a new code only if another pairing attempt is intentionally required.

## 6. Exercise allowlisted execution

After read-only operations pass, explicitly expand the active grant to include allowlisted execution.

For a disposable Git workspace, a low-risk validation command is:

```bash
relmote agent use target-a exec git status
```

**Pass:** the approved command runs inside the approved workspace and returns stdout/stderr/exit status normally.

**Fail:** arbitrary shell execution, commands outside target policy, or an unexpected privilege request becomes available.

## 7. Revoke authority

From the human Controller, revoke the Agent session or disable the relevant Agent/Remote Support authority.

Without repairing or re-pairing the profile, retry:

```bash
relmote agent use target-a status
relmote agent use target-a list .
```

**Pass:** the old credential is rejected after revocation. Connectivity alone must not preserve authority.

This is the primary security success criterion for the baseline test.

## 8. Transport and interruption checks

If time permits, exercise these separately:

- temporarily disable the private transport and confirm operations fail;
- restore transport and confirm authority does not silently broaden;
- stop and restart the Target process and observe session behavior;
- disconnect/reconnect the Agent Host;
- attempt an expired pairing code;
- confirm an unknown target profile fails clearly.

Record ambiguous behavior as a failure or open question rather than interpreting it as success.

## Baseline pass criteria

The baseline Controller → Agent Host → Target validation passes only when all of these are observed:

- [ ] exact build identities recorded;
- [ ] Agent Host capability discovery works;
- [ ] one-time pairing succeeds once;
- [ ] consumed pairing code is rejected;
- [ ] paired target is addressable by profile name;
- [ ] status works;
- [ ] workspace list works;
- [ ] workspace read works;
- [ ] workspace confinement remains enforced;
- [ ] allowlisted execution works only when separately granted;
- [ ] revocation invalidates the previously paired credential;
- [ ] no bearer credential appears in normal CLI output;
- [ ] no unapproved authority appears during the test.

## Result classification

Use one of:

- **PASS** — all baseline pass criteria were observed.
- **PARTIAL** — the path works, but one or more required checks were not exercised.
- **FAIL** — a required operation failed or an authority/security boundary behaved incorrectly.

Do not promote an experimental capability to “implemented and exercised” merely because CI passes. Real-machine behavior is part of this validation.

## After a PASS

After the baseline passes:

1. update [STATUS.md](STATUS.md) with only the capabilities actually exercised;
2. capture reproducible, redacted validation evidence;
3. repeat the test with the Agent Host moved to another machine or platform where practical;
4. cut the next coherent development snapshot if the tested state warrants it;
5. implement the first MCP/Codex adapter on top of the existing paired-target service.

The adapter should initially expose only the already validated operations: target enumeration, target/session status, workspace list/read, and allowlisted execution.
