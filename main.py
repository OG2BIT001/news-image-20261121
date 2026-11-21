#!/usr/bin/env python3
"""Entry program for make.fun competition news-image-20261121.

The artwork lives beside this file as entry.png (drawn by build_art.py).
Running the program copies that file into the output directory under the
name entry.png: /output in the grading sandbox, or the directory named by
MAKEFUN_OUTPUT_DIR for a local run. Because the program only ever copies
one fixed file, two runs write exactly the same bytes.

Standard library only; no network, no clock, no randomness.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent


def main() -> None:
    out_dir = Path(os.environ.get("MAKEFUN_OUTPUT_DIR", "/output"))
    out_dir.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(HERE / "entry.png", out_dir / "entry.png")


if __name__ == "__main__":
    main()
