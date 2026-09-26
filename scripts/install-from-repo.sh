#!/usr/bin/env sh
set -eu

REPO_URL="${RELMOTE_REPO_URL:-https://github.com/dev11systems/relmote.git}"
REF="${RELMOTE_REF:-main}"

die() {
  printf 'Relmote repo installer: %s\n' "$*" >&2
  exit 1
}

command -v python3 >/dev/null 2>&1 ||
  die "Python 3 is required for the current repo preview."

if command -v pipx >/dev/null 2>&1; then
  printf 'Installing Relmote from %s (%s) with pipx...\n' "$REPO_URL" "$REF"
  exec pipx install --force "git+$REPO_URL@$REF"
fi

cat >&2 <<'EOF'
pipx is not installed.

Relmote recommends pipx for repo-based preview installs so it does not modify
your distribution-managed Python environment.

Install pipx using your distribution, for example:

  Debian / Ubuntu / LMDE:
    sudo apt install pipx
    pipx ensurepath

  Fedora:
    sudo dnf install pipx
    pipx ensurepath

Then rerun this installer.

Advanced users may also clone the repository and run:
  ./scripts/preview-linux.sh
EOF
exit 1
