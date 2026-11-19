#!/usr/bin/env python3
"""Entrypoint: copy the pre-rendered infographic to the output directory.

Standard library only. The image is drawn by render.py (run locally, not in
the sandbox); this program only copies the finished file, so both sandbox
runs write identical bytes.
"""
import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))


def main():
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(os.path.join(HERE, "news.png"),
                    os.path.join(out_dir, "entry.png"))


if __name__ == "__main__":
    main()
