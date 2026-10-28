#!/usr/bin/env python3
"""Check release invariants that would break profiles or omit our local fixes."""
import json, os, re
from pathlib import Path
root = Path(__file__).resolve().parent.parent
conf = json.loads((root / "src-tauri/tauri.conf.json").read_text())
pake = json.loads((root / "src-tauri/pake.json").read_text())
node = json.loads((root / "package.json").read_text())
cargo = (root / "src-tauri/Cargo.toml").read_text()
version = conf["version"]
assert node["version"] == version, "Node/Tauri version mismatch"
assert re.search(r'^version = "' + re.escape(version) + r'"$', cargo, re.M), "Cargo/Tauri version mismatch"
assert conf["identifier"] == "com.pake.ab7ae24", "Changing identity changes the session profile"
assert conf["mainBinaryName"] == "pake-whatsapp"
assert pake["windows"][0]["url"] == "https://web.whatsapp.com"
assert pake["windows"][0]["hide_on_close"] and pake["system_tray"]["linux"]
assert 'notify-rust = { path = "../vendor/notify-rust" }' in cargo
assert 'tao = { path = "../vendor/tao" }' in cargo
assert 'notification-diagnostics = ["tauri/devtools"]' in cargo
for fmt in ("deb", "rpm"):
    assert (root / "src-tauri" / conf["bundle"]["linux"][fmt]["desktopTemplate"]).is_file()
for resource in conf["bundle"]["resources"]:
    assert (root / "src-tauri" / resource).is_file(), resource
if os.environ.get("RELEASE_TAG"):
    assert os.environ["RELEASE_TAG"] == "v" + version, "Tag must match configured version"
print(f"Release configuration OK: {version}; both patches and DevTools enabled")
