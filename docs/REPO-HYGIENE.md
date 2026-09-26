# Repository hygiene

Relmote is a general-purpose Dev11 project.

Real-world testing may motivate features, but public documentation, examples, fixtures, and UI copy should describe the generalized product rather than the personal circumstances of individual testers.

## Public examples

Prefer:

- local user;
- helper;
- controller;
- target;
- remote computer;
- test workspace;
- authorized private network.

Avoid embedding:

- tester names;
- family/friend relationships;
- personal device names;
- travel/location context;
- private hostnames;
- private network addresses;
- personal account identifiers.

## Test data

Use synthetic values such as:

```text
target-host
test-project
helper-device
192.0.2.10
2001:db8::10
```

Use documentation address ranges where addresses are needed.

## Reports and fixtures

Before committing captured diagnostics or support reports:

1. inspect the content;
2. remove personal hostnames/usernames;
3. remove real IP/network identifiers where unnecessary;
4. remove secrets/tokens/keys;
5. minimize unrelated machine metadata.

## Development conversations

A feature may originate in a specific support/testing situation.

Translate:

```text
specific situation
→ generalized requirement
→ neutral example
→ repository artifact
```

Do not make the public repository a transcript of the originating conversation.

## Git history

Normal edits remove personal context from current project state but not historical commits.

Do not rewrite published history casually. If genuinely sensitive material is ever committed, treat that as a separate incident requiring appropriate secret/privacy remediation.
