#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
version=$(python3 -c 'import json; print(json.load(open("package.json"))["version"])')
mkdir -p out
git archive --format=tar --prefix="whatsapp-pake-linux-$version/" HEAD | gzip -n > "out/whatsapp-pake-linux-$version-sources.tar.gz"
