# Cellular module

**Likely class:** L

## Purpose

Independent wide-area controller path.

Potential:

- LTE/5G;
- GNSS;
- SIM/eSIM support;
- external antenna option.

## Why module?

Cellular brings:

- regional bands;
- certification;
- carrier variation;
- antenna volume;
- high current bursts;
- rapid modem obsolescence.

It should not determine base Pocket lifetime.

## Controller semantics

Relmote should expose cellular as another authenticated controller path, not as a privileged path.

## Privacy

A cellular module should be optional and physically removable for users who do not want a modem present.
