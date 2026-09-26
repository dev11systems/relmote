# UX decision

## U001 — usability is architecture

Relmote's simple user experience is a core architectural constraint.

The project must not assume users understand networking, SSH, AI agents, capability security, or system administration.

Technical flexibility belongs behind progressive disclosure.

## U002 — one-click common path, composable advanced path

Ordinary support should optimize for:

```text
open → enable → allow → support → stop
```

Advanced users retain access to:

```text
CLI
SSH
Tailscale
custom transports
self-hosting
policy files
module details
developer APIs
```

The advanced path must not dictate the everyday interface.

## U003 — permission comprehension over permission volume

Do not present dozens of low-level capability names to ordinary users.

Group them into understandable actions while preserving exact capability data underneath.

## U004 — safe should not mean painful

If the secure path requires substantially more expertise than the insecure path, redesign the secure path.
