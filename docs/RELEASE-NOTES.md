## 1.0.2 — GTK titlebar dragging fixed

Fixes a regression in 1.0.1: the native GTK titlebar could not move the window because Tao consumed mouse events before GTK handled them. This release backports the remaining upstream propagation and deduplication changes from Tao PR 1218 (commit 07f3742b).

Manually verified by the user on CachyOS/GNOME/Wayland: dragging the window, hiding through X, reopening from the tray, dragging again, and normal clicks inside WhatsApp. The notification fix and enabled DevTools remain unchanged.

### Downloads

- Fedora 44: `.rpm`.
- Ubuntu 22.04+ / compatible Debian: `.deb`.
- Arch / CachyOS: `.pkg.tar.zst`.
- Compatible Linux desktops: `.AppImage` (make executable before running).

The X hides the window to the tray. Use Quit/Sair to exit. DevTools: View → Toggle Developer Tools / Ctrl+Alt+I. Application identity and profile location are preserved during upgrades.

CI compiles and packages all four formats; it does not claim a visual desktop test on every distro. Complete sources and SHA256SUMS are attached. This unofficial Pake-based project is not affiliated with WhatsApp or Meta.
