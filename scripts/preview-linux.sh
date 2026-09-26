#!/usr/bin/env sh
set -eu

# Relmote Linux preview launcher for a checked-out repository.
# It creates an isolated local environment; it does not install a system service.

ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
VENV="$ROOT/.relmote-preview-venv"

if ! command -v python3 >/dev/null 2>&1; then
  echo "Relmote needs Python 3 on this preview build."
  echo "No system service was installed."
  exit 1
fi

if [ ! -x "$VENV/bin/python" ]; then
  echo "Preparing Relmote preview..."
  python3 -m venv "$VENV"
  "$VENV/bin/python" -m pip install --quiet --upgrade pip
  "$VENV/bin/python" -m pip install --quiet -e "$ROOT"
fi

echo "Starting Relmote..."
exec "$VENV/bin/relmote" serve "$@"
