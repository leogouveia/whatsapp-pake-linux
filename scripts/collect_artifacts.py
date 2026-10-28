#!/usr/bin/env python3
import json, os, shutil, sys
from pathlib import Path
root = Path(__file__).resolve().parent.parent
version = json.loads((root / "src-tauri/tauri.conf.json").read_text())["version"]
fmt = sys.argv[1]
ext = {"deb": ".deb", "rpm": ".rpm", "appimage": ".AppImage"}[fmt]
files = list((root / "src-tauri/target/release/bundle" / fmt).glob("*" + ext))
if len(files) != 1:
    raise SystemExit(f"Expected exactly one {fmt} bundle, found {files}")
flavor = os.environ.get("BUILD_FLAVOR", "linux")
out = root / "out"
out.mkdir(exist_ok=True)
target = out / f"whatsapp-pake-linux-{version}-{flavor}-x86_64{ext}"
shutil.copy2(files[0], target)
print(target)
