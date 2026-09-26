#!/usr/bin/env sh
set -eu

# Development/temporary launcher. Does not install an OS service.
exec python -m relmote.cli serve "$@"
