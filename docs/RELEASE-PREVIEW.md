# Preview release strategy

The first public/tester artifact should optimize for **trying Relmote**, not installing a permanent management stack.

## Linux artifacts

Initial targets:

- x86-64;
- ARM64 after the build is validated.

## Desired user flow

```text
Download Relmote Preview
→ run
→ browser opens
→ Check This Computer / Enable Support
```

No Git checkout or Python package knowledge.

## Build strategy

The repository should produce a self-contained executable artifact in CI.

A bundled executable is the first experiment because it:

- minimizes tester prerequisites;
- keeps temporary mode temporary;
- can later be wrapped in AppImage/package formats;
- lets us validate application behavior before committing to distro packaging.

## Artifact requirements

- generated from tagged/reviewable source;
- include version/commit metadata;
- no auto-start service;
- localhost by default;
- no public listener by default;
- easy to delete;
- checksum published with release.

## Later packaging

Evaluate:

- AppImage;
- deb/rpm;
- Flatpak if appropriate;
- distro/community packages.

Packaging format should not become part of the Relmote protocol.
