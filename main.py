#!/usr/bin/env python3
"""Make.fun entry program for the "news-image-20261120" bounty.

Copies the rendered newspaper front page (entry.png, stored next to this
script) into the output directory as entry.png and verifies the result.

Standard library only.
"""

from __future__ import annotations

import os
import shutil
import sys
from pathlib import Path

PNG_MAGIC = b"\x89PNG\r\n\x1a\n"
SOURCE_NAME = "entry.png"
OUTPUT_NAME = "entry.png"


def main() -> int:
    source = Path(__file__).resolve().parent / SOURCE_NAME
    output_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    destination = output_dir / OUTPUT_NAME

    if not source.is_file():
        print(f"error: source image not found: {source}", file=sys.stderr)
        return 1

    output_dir.mkdir(parents=True, exist_ok=True)

    # copyfile (not copy2) keeps the output bytes exactly identical to the source.
    shutil.copyfile(source, destination)

    byte_count = destination.stat().st_size
    with destination.open("rb") as handle:
        header = handle.read(len(PNG_MAGIC))

    if byte_count <= 0:
        print(f"error: copied file is empty: {destination}", file=sys.stderr)
        return 1
    if header != PNG_MAGIC:
        print(f"error: copied file is not a PNG: {destination}", file=sys.stderr)
        return 1

    # Validate dimensions from the IHDR chunk: 8-byte signature, 4-byte length,
    # 4-byte type ("IHDR"), then 4-byte width and 4-byte height.
    with destination.open("rb") as handle:
        ihdr = handle.read(24)
    if len(ihdr) < 24 or ihdr[12:16] != b"IHDR":
        print(f"error: could not read PNG IHDR chunk: {destination}", file=sys.stderr)
        return 1
    width = int.from_bytes(ihdr[16:20], "big")
    height = int.from_bytes(ihdr[20:24], "big")
    if width != 1024 or height != 1024:
        print(
            f"error: unexpected PNG dimensions {width}x{height} "
            f"(expected 1024x1024): {destination}",
            file=sys.stderr,
        )
        return 1

    print(f"source:      {source}")
    print(f"destination: {destination}")
    print(f"bytes:       {byte_count}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
