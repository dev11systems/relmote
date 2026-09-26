# Interactive sessions

Relmote exposes interactive capabilities through explicit sessions rather than by granting a controller unrestricted access to a node.

The same model applies to software and hardware implementations.

## Session families

### Terminal

A terminal session grants an approved controller interactive access to one terminal endpoint at a defined authority level.

Possible backends include:

- local software PTY;
- SSH;
- serial console;
- container/VM console;
- hardware serial module;
- future KVM text/console adapters.

### Screen

A screen session grants observation or control of one graphical/video endpoint.

Possible backends include:

- Wayland ScreenCast portal + PipeWire;
- X11 adapter;
- operating-system native screen-sharing APIs;
- hardware HDMI/DisplayPort/USB video capture;
- KVM module;
- VM display console.

The controller should not need to know whether the pixels came from a software portal or a hardware capture module.

## Authority layers

Interactive access may require several independent approvals.

For example, Wayland Screen Observe:

1. Relmote remote support must be available.
2. Controller requests Screen Observe.
3. Relmote policy/session layer approves the request.
4. The desktop OS presents its own screen/window chooser and consent.
5. Only after OS consent does the session become ACTIVE.

Relmote must not treat network reachability as authorization or attempt to bypass the operating system's consent boundary.

## States

A backend may use additional intermediate states, but the common lifecycle is:

```text
requested
   ↓
approved
   ↓
backend/os consent
   ↓
active
   ↓
ended
```

Failure at any step must be visible to the controller and must not leave the session marked active.

## Observe vs control

Screen observation and input control are separate capabilities.

An Observe grant must never imply mouse/keyboard control.

Likewise, a terminal session is not equivalent to graphical control or administrative privilege.

## Hardware/software parity

Hardware Relmote should implement the same semantic objects.

A future KVM module may advertise:

```text
screen.observe
input.keyboard
input.pointer
```

while a Linux software node may advertise:

```text
screen.observe.portal
terminal.user
```

The controller can then present one coherent UX while accurately describing the active backend and authority.
