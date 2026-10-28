# Package layouts

Tauri generates DEB, RPM and AppImage using `src-tauri/tauri.conf.json`.
The Arch recipe is `scripts/package_arch.py`: it creates the pacman archive
from a binary compiled natively on Arch, with `.PKGINFO`, icons, desktop entry,
resources and license notices. It does not invoke pacman or install anything.

Package name: `whatsapp`; executable: `pake-whatsapp`;
application/profile identifier: `com.pake.ab7ae24`.

All artifacts go to the ignored `out/` directory. Never commit generated
binaries, build caches, profiles, logs, cookies or WhatsApp session files.
