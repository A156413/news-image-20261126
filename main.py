#!/usr/bin/env python3
"""Ship the 26 November 2026 world-news image to /output/entry.png
for make.fun's 'news-image-20261126' bounty.

The front page was painted locally by draw_poster.py in this repo
(where Pillow and DejaVu fonts exist) and committed as entry.png.
This program only copies that committed poster into the directory
the grader names, using the standard library and nothing else.

Why copy instead of draw: the grader's pinned Python image has
neither Pillow nor the DejaVu fonts, so drawing at runtime exits 1
— exactly what killed the first 20261125 attempt (submission
01a2107e). The 23, 24 and 25 November editions all shipped with
this copy pattern and passed.

The day in the picture: Pyongyang expels Switzerland's diplomat
and orders its office shut; Pakistan's first astronaut reaches
China's Tiangong station on Shenzhou-24; Colombian police free 20
hostages after a 17-hour supermarket siege; Australia and Solomon
Islands sign a landmark security pact; Bangladesh garment workers
win a 36% pay rise; plus Nepal's quake, Russia's war dead near
500,000, US consumer confidence and Bellingham's wondergoal.
"""

import os
import shutil
import struct

POSTER = "entry.png"
SIDE = 1024
MAGIC = b"\x89PNG\r\n\x1a\n"


def read_ihdr(path):
    """Return (width, height) from a PNG's IHDR chunk, stdlib only."""
    with open(path, "rb") as handle:
        head = handle.read(24)
    if head[:8] != MAGIC:
        raise SystemExit(f"{path}: not a PNG file")
    if head[12:16] != b"IHDR":
        raise SystemExit(f"{path}: no IHDR chunk where expected")
    width, height = struct.unpack(">II", head[16:24])
    return width, height


def main():
    repo = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(repo, POSTER)
    if not os.path.isfile(source):
        raise SystemExit(f"committed poster not found: {source}")
    width, height = read_ihdr(source)
    if (width, height) != (SIDE, SIDE):
        raise SystemExit(
            f"poster is {width}x{height}, expected {SIDE}x{SIDE}")
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, POSTER)
    shutil.copyfile(source, target)
    if os.path.getsize(target) != os.path.getsize(source):
        raise SystemExit("entry.png copy came out short")
    # the grader collects outputs as another user: leave it readable
    os.chmod(target, 0o644)
    print(f"wrote {target} ({os.path.getsize(target)} bytes, "
          f"{width}x{height}, from committed {os.path.getsize(source)} bytes)")


if __name__ == "__main__":
    main()
