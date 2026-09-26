# Identity recovery

Recovery balances two goals:

1. losing a phone should not permanently lock an owner out;
2. recovery must not become a universal backdoor.

## Controller loss

Revoke the lost controller key, use another owner controller, and pair a replacement.

## Owner recovery strategies

### Recovery key

Generate an offline recovery credential stored by the owner, such as printed material, encrypted removable storage, or a password manager.

### Multiple owner devices

Several controllers can independently hold owner authority.

### Recovery quorum

Future option for shared/community infrastructure: require a threshold such as two of three recovery principals.

### Physical node recovery

Hardware Relmotes may expose a deliberate local recovery ceremony using physical access, controls, recovery port, and explicit reset.

A physical reset may erase trust state rather than magically restore old secrets.

## Optional Dev11-assisted recovery

If Dev11 ever offers account sync/recovery, it must not be the only mechanism.

## Backup

Identity backups should be encrypted, exportable, versioned, and restorable without a proprietary cloud.

## Node reset

A full identity reset creates a new node identity. Previously paired controllers should see that identity changed rather than silently trusting the replacement.

## Target credentials

Relmote identity recovery is separate from recovering target passwords, SSH keys, or other target credentials.
