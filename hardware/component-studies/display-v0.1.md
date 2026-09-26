# Display study v0.1

Pocket needs a display for **state**, not for becoming a tiny smartphone.

## Requirements

- readable at a glance;
- low idle power;
- readable in varied lighting;
- enough refresh speed for state/activity;
- available in ~2–2.4 inch class;
- not required for safety-critical STOP;
- replaceable.

## Candidate classes

### Memory / reflective LCD

Strengths:

- extremely low static-image power;
- sunlight readability;
- good for always-visible state.

Weaknesses:

- module availability/cost;
- color/contrast options vary;
- front-light may be needed in darkness.

**Fit:** conceptually excellent.

### Monochrome OLED

Strengths:

- compact;
- high contrast;
- inexpensive/common;
- easy prototype integration.

Weaknesses:

- emissive idle power;
- burn-in/lifetime considerations;
- sunlight performance.

**Fit:** excellent prototype, less obviously ideal production choice.

### Conventional TFT LCD

Strengths:

- cheap;
- broad availability;
- color;
- fast.

Weaknesses:

- backlight power;
- thicker optical stack;
- less compelling for always-on status.

**Fit:** acceptable, especially All-in-One.

### E-paper

Strengths:

- near-zero static-image display power;
- excellent sunlight readability.

Weaknesses:

- slow refresh;
- ghosting;
- poor activity feedback;
- temperature-dependent behavior.

**Fit:** interesting secondary/status surface, probably not sole Pocket UI.

## v0.1 recommendation

Keep the **52 × 28 mm visible window** and do not freeze technology.

Prototype UI first on readily available OLED/TFT hardware.

In parallel, evaluate reflective/memory LCD for production Pocket.

## UI constraint

Critical state must also exist outside the application display:

- ARMED hardware indicator;
- STOP/fault hardware indication;
- physical AUTHORIZE;
- physical STOP.
