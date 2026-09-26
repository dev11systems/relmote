# Screen observe and control

Screen access is a first-class Relmote capability with separate authority for **viewing** and **controlling**.

## Capabilities

Conceptually:

```text
screen.observe
input.pointer
input.keyboard
```

A grant to view the screen does not imply permission to send input.

## Linux

Linux screen support must account for both Wayland and X11.

### Wayland

Prefer desktop-supported consent/security mechanisms where available, including:

- xdg-desktop-portal;
- PipeWire streams;
- desktop/session APIs appropriate to the environment.

Do not design Relmote around silently bypassing Wayland's security model.

### X11

An X11 adapter may use appropriate capture/input mechanisms when the local user's session permits them.

X11 and Wayland are implementation adapters behind the same Relmote capability model.

## User experience

Target:

```text
SCREEN

Helper can:
✓ View screen

Control:
○ Off

[ Allow keyboard/mouse control ]
[ Stop screen sharing ]
```

When control is requested:

```text
A helper wants to control the pointer and keyboard.

[ Allow once ]
[ Allow for this session ]
[ Deny ]
```

## Browser controller

The web controller should eventually provide:

- live screen surface;
- fit/scale controls;
- pointer input when permitted;
- keyboard input when permitted;
- visible latency/connection state;
- immediate stop/revoke.

## Privacy

The target should have a persistent visible indication while screen observation/control is active.

Stopping support must stop screen streaming and input authority.

## Evidence and audit

Record session/control events, not captured screen contents by default.

Do not silently retain screenshots/video as an audit mechanism.

## Backend interface

Screen capture and input injection should be replaceable adapters.

Potential backends include:

- Linux Wayland portal/PipeWire;
- Linux X11;
- macOS native screen-capture/accessibility APIs;
- Windows native capture/input APIs;
- hardware KVM/Pocket.

The Relmote protocol should not assume one backend.
