Unofficial WhatsApp Web desktop app based on Pake, with Linux integration fixes and DevTools enabled.

Included fixes:
- Persistent D-Bus notification connection for GNOME.
- Native GTK window decorations on Wayland.
- DevTools available through View → Toggle Developer Tools / Ctrl+Alt+I.

Choose one installer:
- Fedora 44: `.rpm`.
- Ubuntu 22.04+ / compatible Debian: `.deb`.
- Arch / CachyOS: `.pkg.tar.zst`.
- Compatible Linux desktops: `.AppImage` (make executable before running).

The X hides the window to the tray. Use Quit/Sair to exit. GNOME tray integration may require an AppIndicator extension.

Manual behavior was validated in the original local build on CachyOS/GNOME 51.1/Wayland. CI compiles and packages the other formats; it does not claim a visual desktop test on every distro. See the README and docs for compatibility and installation details.

The source archive includes both patched dependencies and build scripts. SHA256SUMS covers the release downloads. No login/session data is included. This project is not affiliated with WhatsApp or Meta.
