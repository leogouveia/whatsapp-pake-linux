# Contributing

Start with docs/BUILD.md and docs/PROVENANCE.md. Preserve the application identity unless a migration is intentional and documented. Keep patches narrow, preserve upstream notices, and explain whether a fix was tested manually or only compiled.

For bug reports include distro/version, desktop, Wayland/X11, package format, application version and a minimal reproduction. For notification issues use a synthetic title/body. Do not attach cookies, tokens, chats or full browser storage dumps.

Pull requests run configuration checks. Release tags run native package builds in the documented environments. Changes to a vendored crate should update its reviewable diff in patches/ and describe the relation to upstream fixes.
