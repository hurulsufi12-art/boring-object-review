"""One-line review of the most boring everyday object.

Writes a single funny, true review to /output/entry.txt.

Gate (from RULES.txt): the file must be UTF-8 text of 1 to 200
characters, not only white space. The judge brief adds that it must be
one line, so this program also refuses newlines and control characters.
Validation runs before anything is written; an invalid review exits
non-zero and writes no file.
"""

import sys
from pathlib import Path

# The review: a plain white sock. Its twin really does vanish in the
# wash, the survivor really does go grey, and its whole job really is
# holding up one foot -- so the dullness itself is the joke.
REVIEW = (
    "My plain white sock lost its twin to the dryer years ago; "
    "now it just goes grey alone, holding up one foot and a lifelong grudge."
)

MAX_CHARS = 200
DEFAULT_OUTPUT = Path("/output/entry.txt")


def validate_review(text):
    """Check one review against the gate; raise ValueError if it fails."""
    if not isinstance(text, str):
        raise ValueError("review must be text, not %s" % type(text).__name__)
    if not text.strip():
        raise ValueError("review is empty or only whitespace")
    if len(text) > MAX_CHARS:
        raise ValueError(
            "review is %d characters, over the 200-character limit"
            % len(text)
        )
    for ch in text:
        if ch in ("\n", "\r") or ord(ch) < 32 or ord(ch) == 127:
            raise ValueError(
                "review must be a single line without control characters"
            )
    return text


def write_entry(path):
    """Validate REVIEW, then write it as UTF-8 with no trailing newline."""
    checked = validate_review(REVIEW)
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_bytes(checked.encode("utf-8"))
    return target


def main(argv=None):
    """Entry point: validate first, write second, never write invalid."""
    args = list(sys.argv[1:] if argv is None else argv)
    dest = DEFAULT_OUTPUT
    if "--output" in args:
        idx = args.index("--output")
        if idx + 1 >= len(args):
            print("error: --output needs a path", file=sys.stderr)
            return 2
        dest = Path(args[idx + 1])
    try:
        write_entry(dest)
    except ValueError as exc:
        print("error: invalid review: %s" % exc, file=sys.stderr)
        return 1
    except OSError as exc:
        print("error: cannot write %s: %s" % (dest, exc), file=sys.stderr)
        return 1
    print("wrote %d characters to %s" % (len(REVIEW), dest))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

