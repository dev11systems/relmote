#!/usr/bin/env sh
set -eu

REPO="${RELMOTE_REPO:-dev11systems/relmote}"
INSTALL_DIR="${RELMOTE_INSTALL_DIR:-$HOME/.local/bin}"
VERSION="${RELMOTE_VERSION:-latest}"

die() {
  printf 'Relmote installer: %s\n' "$*" >&2
  exit 1
}

need() {
  command -v "$1" >/dev/null 2>&1 || die "required command not found: $1"
}

need uname
need mktemp
need sha256sum

case "$(uname -s)" in
  Linux) ;;
  *) die "this preview installer currently supports Linux only" ;;
esac

case "$(uname -m)" in
  x86_64|amd64)
    ARCH="x86_64"
    ;;
  aarch64|arm64)
    ARCH="arm64"
    ;;
  *)
    die "unsupported architecture: $(uname -m)"
    ;;
esac

if command -v curl >/dev/null 2>&1; then
  fetch() { curl -fL --proto '=https' --tlsv1.2 "$1" -o "$2"; }
elif command -v wget >/dev/null 2>&1; then
  fetch() { wget --https-only -O "$2" "$1"; }
else
  die "curl or wget is required"
fi

if [ "$VERSION" = "latest" ]; then
  BASE="https://github.com/$REPO/releases/latest/download"
else
  BASE="https://github.com/$REPO/releases/download/$VERSION"
fi

BINARY="relmote-linux-$ARCH"
TMP="$(mktemp -d)"
trap 'rm -rf "$TMP"' EXIT HUP INT TERM

printf 'Downloading Relmote for Linux %s...\n' "$ARCH"
fetch "$BASE/$BINARY" "$TMP/$BINARY"
fetch "$BASE/SHA256SUMS" "$TMP/SHA256SUMS"

(
  cd "$TMP"
  grep "  $BINARY$" SHA256SUMS > SHA256SUMS.selected ||
    die "checksum for $BINARY not found"
  sha256sum -c SHA256SUMS.selected
)

mkdir -p "$INSTALL_DIR"
install -m 0755 "$TMP/$BINARY" "$INSTALL_DIR/relmote"

printf '\nRelmote installed to:\n  %s/relmote\n\n' "$INSTALL_DIR"
case ":$PATH:" in
  *":$INSTALL_DIR:"*) ;;
  *)
    printf 'Add this directory to PATH if needed:\n  %s\n\n' "$INSTALL_DIR"
    ;;
esac

"$INSTALL_DIR/relmote" version || true

cat <<EOF

Installation does NOT enable remote support or install a background service.

Run:
  relmote

To remove this portable install:
  rm "$INSTALL_DIR/relmote"
EOF
