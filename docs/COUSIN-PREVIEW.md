# Cousin Preview

**Goal:** a testable Relmote Software Preview within days, on an ordinary computer, without installing a persistent remote-management service.

## Preview promise

The preview should let someone:

1. run Relmote temporarily;
2. open the local browser UI;
3. see which machine/node they are using;
4. start an explicit Observe session;
5. run useful read-only diagnostics;
6. see findings separately from evidence;
7. export a support report;
8. revoke the session;
9. quit Relmote and leave no background service.

## Security boundary

Preview defaults:

- localhost only;
- no LAN listener;
- no public listener;
- no arbitrary shell;
- no write actions;
- no unattended access;
- no cloud account;
- no AI required.

This means the first preview is best tested **while physically using the target computer**.

Remote/iPad control follows after pairing/authentication.

## Must-have before preview tag

- [x] localhost browser UI
- [x] ephemeral node identity
- [x] explicit Observe session
- [x] revoke
- [x] system overview
- [x] network overview
- [x] deterministic network diagnosis
- [x] storage overview
- [x] findings vs raw evidence
- [ ] platform adapter for the cousin's target OS
- [ ] support-report export
- [ ] self-check page/command
- [ ] friendly temporary launcher
- [ ] manual smoke test on the target OS
- [ ] preview release/tag

## Nice-to-have

- process overview;
- service overview;
- richer interface/route/DNS observations;
- browser auto-open;
- single-file executable.

## Explicitly after preview

- LAN controller;
- QR pairing;
- remote access;
- state-changing actions;
- AI planner;
- persistent Agent service.

## Test script

During the visit:

1. Launch Relmote.
2. Confirm browser opens only on localhost.
3. Record node fingerprint.
4. Start Observe.
5. Run System overview.
6. Run Network overview.
7. Run Diagnose network.
8. Run Storage overview.
9. Verify claims match the machine.
10. Inspect raw evidence.
11. Export support report.
12. Revoke.
13. Confirm tasks no longer run.
14. Quit Relmote.
15. Confirm no background service remains.

Record confusing UI, missing diagnostics, incorrect claims, and OS-specific failures.
