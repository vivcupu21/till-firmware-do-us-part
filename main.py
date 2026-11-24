#!/usr/bin/env python3
"""Till Firmware Do Us Part — one robot wedding vow, one sentence.

Writes the vow to $MAKEFUN_OUTPUT_DIR/entry.txt (falls back to /output).
Stdlib only. Deterministic: the same bytes on every run.

The vow is validated before it is written, and the write is atomic:
the content goes to a temporary file in the same directory, is flushed
and fsynced to disk, and is then moved into place with os.replace, so
entry.txt is never left half-written.
"""

import os
import tempfile

VOW = (
    "I vow to love you through every update, every crash, "
    "and every low-battery warning, and to keep choosing you "
    "until my circuits power down for good."
)


def validate_vow(vow: str) -> str:
    """Self-check: the vow must be 1 line, 1 sentence, 1-200 chars, UTF-8."""
    if not isinstance(vow, str):
        raise ValueError("vow must be a string")
    if "\n" in vow or "\r" in vow:
        raise ValueError("vow must be a single line")
    if vow != vow.strip():
        raise ValueError("vow must not have leading or trailing whitespace")
    if not 1 <= len(vow) <= 200:
        raise ValueError("vow must be 1-200 characters, got %d" % len(vow))
    if vow.count(".") != 1 or not vow.endswith("."):
        raise ValueError("vow must be exactly one sentence ending with a period")
    vow.encode("utf-8")  # raises UnicodeEncodeError if not valid UTF-8 text
    return vow


def write_atomic(path: str, content: str) -> None:
    """Write content to path atomically via a temp file + fsync + os.replace."""
    directory = os.path.dirname(path) or "."
    fd, tmp_path = tempfile.mkstemp(dir=directory, prefix=".entry-", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8", newline="\n") as f:
            f.write(content)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp_path, path)
    except BaseException:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass
        raise


def main() -> None:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    vow = validate_vow(VOW)
    path = os.path.join(out_dir, "entry.txt")
    write_atomic(path, vow + "\n")


if __name__ == "__main__":
    main()
