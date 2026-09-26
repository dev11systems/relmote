# SSH Preview

Relmote does not need to implement an SSH server to be useful over SSH.

## Model

```text
controller
   │
   │ existing OpenSSH
   ▼
target computer
   │
   └─ relmote CLI
```

Authentication, host keys, encryption, and account policy remain the responsibility of the host's SSH service.

## Preview commands

```text
relmote status
relmote diagnose network
```

These are read-only.

## Why this is useful

During early testing, SSH gives us:

- encrypted remote access;
- mature authentication;
- no new listening daemon;
- easy testing from another laptop/tablet SSH client.

It also proves that the Relmote semantic layer can have multiple controllers:

- browser;
- CLI over local terminal;
- CLI over SSH.

## What this is not

Relmote does not:

- enable SSH automatically;
- modify sshd configuration;
- create OS accounts;
- bypass host authentication.

If SSH is disabled, LAN browser preview can still be used.
