# Debugging and logs

Relmote keeps a small rotating per-user debug log for preview troubleshooting.

## Location

On XDG-style environments:

```text
$XDG_STATE_HOME/relmote/relmote.log
```

When `XDG_STATE_HOME` is not set:

```text
~/.local/state/relmote/relmote.log
```

The active file is limited to roughly 1 MB with three rotated backups.

## CLI

Show the most recent 100 lines:

```bash
relmote logs
```

Show more:

```bash
relmote logs --tail 300
```

Print only the internal log path:

```bash
relmote logs --path
```

Save the full active log to an ordinary file in the current directory:

```bash
relmote logs --save
```

This creates:

```text
./relmote-debug.log
```

Save to a specific location:

```bash
relmote logs --save ~/relmote-debug.txt
```

Save only the most recent lines:

```bash
relmote logs --tail 200 --save ~/relmote-debug.txt
```

The save form is useful on mobile/remote terminal clients where selecting and copying large terminal scrollback is awkward. The exported file is a copy or excerpt of the active debug log; rotated backups are not included.

## Privacy

Logs are local to the current user and are not automatically uploaded.

Inspect them before sharing. Debug output may contain hostnames, filesystem paths, private network details, tool stderr, or other machine-specific information. Relmote should avoid deliberately logging bearer credentials, pairing codes, typed terminal contents, or file contents.

The structured audit log and support report are separate from this debug log:

- **debug log** — software failures and operational troubleshooting;
- **audit log** — authority/action events, intentionally metadata-oriented;
- **support report** — an explicit export of current diagnostic state.

These should remain separate so troubleshooting does not silently become surveillance or content logging.
