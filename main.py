#!/usr/bin/env python3
"""Monday Morning Punchlines - make.fun bounty entry.

Writes one joke about Monday mornings to /output/entry.txt.
Fully deterministic: no randomness, no time, no network, no input.
The joke is a fixed string.

Usage: python3 main.py [output-path]
With no argument, the output goes to $MAKEFUN_OUT_DIR, then $MAKEFUN_OUT,
then /output/entry.txt. With an argument, that path is used instead: a
directory argument means <directory>/entry.txt, a file argument is used
as the output file itself.
"""

import os
import sys

JOKE = "Monday installed an update overnight. My motivation now runs on a free trial that expired at 6am."

MIN_CHARS = 1
MAX_CHARS = 200


def resolve_output_path() -> str:
    """Return the output file path from argv, the environment, or default."""
    if len(sys.argv) > 1:
        # An explicit output path wins over the environment and default.
        # A directory (existing, or ending in a separator) means
        # <directory>/entry.txt; anything else is the output file itself.
        given = sys.argv[1]
        if given.endswith(os.sep) or os.path.isdir(given):
            return os.path.join(given, "entry.txt")
        return given
    out_dir = os.environ.get("MAKEFUN_OUT_DIR") or os.environ.get("MAKEFUN_OUT") or "/output"
    return os.path.join(out_dir, "entry.txt")


def write_entry() -> tuple[str, int]:
    """Write the joke to the resolved output path; return (path, chars)."""
    path = resolve_output_path()
    parent = os.path.dirname(path) or "."
    os.makedirs(parent, exist_ok=True)
    with open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(JOKE + "\n")
    return path, len(JOKE)


def main() -> int:
    chars = len(JOKE)
    if not MIN_CHARS <= chars <= MAX_CHARS:
        print(f"joke is {chars} characters, outside 1-200", file=sys.stderr)
        return 1
    if not JOKE.strip():
        print("joke is only white space", file=sys.stderr)
        return 1
    path, chars = write_entry()
    print(f"wrote {chars} characters to {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
