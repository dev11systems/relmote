# Software Preview Test

**Goal:** validate a testable Relmote Software Preview on an ordinary computer without requiring a persistent remote-management service.

## Preview promise

The preview should let a tester:

1. run Relmote temporarily;
2. open the local browser UI;
3. identify the current node/target;
4. run useful read-only diagnostics;
5. see findings separately from evidence;
6. export a support report;
7. stop/revoke activity;
8. quit Relmote without leaving a background service.

## Remote test

When an authorized private network already exists, a preferred remote preview is:

```text
Relmote localhost
→ private-network exposure or explicit private-interface binding
→ authorized controller
```

Relmote may remain installed between support sessions.

Availability can be disabled, timed, or enabled until manually disabled. Availability remains separate from capability grants.

## Security boundary

Preview defaults favor:

- localhost;
- no public listener;
- no arbitrary shell;
- read-only diagnostics first;
- no unattended access;
- no mandatory cloud account;
- no AI requirement.

## Test script

1. Launch Relmote.
2. Record version and run `relmote doctor`.
3. Run Full Check.
4. Run focused network/storage checks.
5. Verify claims against the machine.
6. Inspect raw evidence.
7. Export and inspect a support report.
8. Verify local TUI/web state is consistent.
9. Quit Relmote.
10. Confirm no unintended background service remains.

Record confusing UI, missing diagnostics, incorrect claims, and platform-specific failures.
