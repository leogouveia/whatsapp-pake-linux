#!/usr/bin/env python3
import json, os, platform, shutil, subprocess, tempfile, time
from pathlib import Path
root = Path(__file__).resolve().parent.parent
if platform.machine() != "x86_64":
    raise SystemExit("This release recipe currently supports x86_64 only")
version = json.loads((root / "src-tauri/tauri.conf.json").read_text())["version"]
binary = root / "src-tauri/target/release/pake"
if not binary.is_file():
    raise SystemExit("Build src-tauri with cargo build --locked --release first")
out = root / "out"
out.mkdir(exist_ok=True)
package = out / f"whatsapp-{version}-1-x86_64.pkg.tar.zst"
with tempfile.TemporaryDirectory(prefix="whatsapp-arch-") as temp:
    stage = Path(temp)
    def install(source, target, mode=0o644):
        dest = stage / target
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, dest)
        dest.chmod(mode)
    install(binary, "usr/bin/pake-whatsapp", 0o755)
    for dest in ("usr/lib/whatsapp/png/whatsapp_512.png", "usr/share/icons/hicolor/512x512/apps/pake-whatsapp.png"):
        install(root / "src-tauri/png/whatsapp_512.png", dest)
    install(root / "src-tauri/assets/whatsapp.desktop", "usr/share/applications/whatsapp.desktop")
    for name in ("LICENSE", "LICENSE-EXCEPTION", "THIRD_PARTY.md"):
        install(root / name, "usr/share/licenses/whatsapp/" + name)
    size = sum(p.stat().st_size for p in stage.rglob("*") if p.is_file())
    deps = ["cairo", "desktop-file-utils", "gdk-pixbuf2", "glib2", "gtk3", "hicolor-icon-theme", "libappindicator-gtk3", "libsoup3", "pango", "webkit2gtk-4.1"]
    metadata = f"pkgname = whatsapp\npkgbase = whatsapp\npkgver = {version}-1\npkgdesc = Unofficial WhatsApp Pake app with Linux fixes and DevTools\nurl = https://github.com/leogouveia/whatsapp-pake-linux\nbuilddate = {os.environ.get('SOURCE_DATE_EPOCH', int(time.time()))}\npackager = leogouveia\nsize = {size}\narch = x86_64\nlicense = GPL-3.0-or-later\n"
    metadata += "".join("depend = " + dep + "\n" for dep in deps)
    (stage / ".PKGINFO").write_text(metadata)
    subprocess.run(["bsdtar", "--zstd", "--uid", "0", "--gid", "0", "--uname", "root", "--gname", "root", "-cf", str(package), "-C", str(stage), ".PKGINFO", "usr"], check=True)
print(package)
