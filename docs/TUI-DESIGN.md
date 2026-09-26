# TUI design

The Relmote TUI should make terminal operation approachable without becoming a graphical UI awkwardly recreated in characters.

## Home

```text
RELMOTE — this computer

Support        OFF
Helper         Rae
Connection     Private

What would you like to do?

  Check this computer
  Diagnose a problem
  Projects
  Support settings
  Technical details
```

## Full check

```text
CHECK THIS COMPUTER

✓ System       Linux detected
✓ Services     No failed services
⚠ Storage      91% used
✓ Network      Address configured
○ Internet     Not tested

> Test Internet connection
  View details
  Back
```

## Permission

```text
REVIEW REQUEST

Rae wants to edit:

  Test Project / README.md

  - old line
  + new line

This changes one file.

> Allow this change
  Deny
  Technical details
```

## Advanced mode

Technical users can switch to a denser view showing:

- target IDs;
- transport;
- capability names;
- hashes;
- task IDs;
- evidence references.

Do not make Advanced mode a separate application.

## SSH

The TUI should work naturally after:

```text
ssh target
relmote
```

No browser forwarding required.

## Implementation

Do not freeze a TUI framework until the interaction model is tested.

Candidates can be evaluated for:

- accessibility;
- binary bundling;
- terminal compatibility;
- dependency weight;
- async/event support;
- testability.
