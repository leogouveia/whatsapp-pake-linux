#!/usr/bin/env bash
set -euo pipefail
ROOT=$(CDPATH= cd -- "$(dirname -- "$0")/.." && pwd)
cd "$ROOT"
format=${1:-}
python3 scripts/validate.py
case "$format" in
  arch)
    (cd src-tauri && cargo build --locked --release --features notification-diagnostics)
    python3 scripts/package_arch.py
    ;;
  deb|rpm|appimage)
    npm run tauri -- build --bundles "$format" --features notification-diagnostics -- --locked
    python3 scripts/collect_artifacts.py "$format"
    ;;
  *) printf 'Usage: %s {arch|deb|rpm|appimage}\n' "$0" >&2; exit 2 ;;
esac
