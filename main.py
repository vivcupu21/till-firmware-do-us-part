#!/usr/bin/env python3
"""Till Firmware Do Us Part — one robot wedding vow, one sentence.

Writes the vow to $MAKEFUN_OUTPUT_DIR/entry.txt (falls back to /output).
Stdlib only. Deterministic: the same bytes on every run.
"""

import os

VOW = (
    "I vow to love you through every update, every crash, "
    "and every low-battery warning, and to keep choosing you "
    "until my circuits power down for good."
)


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.txt")
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(VOW + "\n")


if __name__ == "__main__":
    main()
