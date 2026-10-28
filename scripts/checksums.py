#!/usr/bin/env python3
import hashlib, sys
from pathlib import Path
folder = Path(sys.argv[1] if len(sys.argv) > 1 else "out")
files = sorted(p for p in folder.iterdir() if p.is_file() and p.name != "SHA256SUMS")
with (folder / "SHA256SUMS").open("w") as output:
    for p in files:
        output.write(hashlib.sha256(p.read_bytes()).hexdigest() + "  " + p.name + "\n")
print(folder / "SHA256SUMS")
