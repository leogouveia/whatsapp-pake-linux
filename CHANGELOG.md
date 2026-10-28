# Changelog

## 1.0.1 — 2026-10-28

First public source snapshot and automated multi-format release pipeline.

- Preserve a D-Bus connection in notify-rust so GNOME does not immediately remove app-associated notifications.
- Use native GTK decorations instead of Tao's custom Wayland header.
- Keep DevTools enabled in optimized builds.
- Preserve the existing application identity and WhatsApp profile location.
- Add Fedora RPM, Ubuntu DEB/AppImage and native Arch package jobs.
- Publish complete sources and SHA256 checksums only after all four packages build.
- Document the original diagnosis, known validation, build-from-source instructions and maintenance process.

Manual validation on CachyOS/GNOME 51.1/Wayland: synthetic notification, real incoming message, D-Bus sender alive for 30 seconds, and close/reopen/close via tray. Other desktops still require manual validation.
