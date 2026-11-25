"""The Battery's Last Text to Its Charger — make.fun entry.

Writes one line of plain text (at most 200 characters): the phone
battery's last text message to the charger it waited for all day,
to $MAKEFUN_OUTPUT_DIR/entry.txt (default /output/entry.txt).

Pure standard library only.
"""

import os

MESSAGE = (
    "I held 1% all day for one more boss fight. You're welcome. "
    "My last act: the save file is gone."
)

MAX_CHARS = 200


def validate(text):
    """Enforce the RULES.txt gate: UTF-8, 1-200 chars, not only whitespace.

    Also rejects leading/trailing whitespace (wasted bytes on the
    size tie-break) and C0 control characters / DEL, which would
    corrupt the single clean line the judge reads.
    """
    if not isinstance(text, str):
        raise ValueError("entry must be text")
    if not text.strip():
        raise ValueError("entry must not be only whitespace")
    if "\n" in text or "\r" in text:
        raise ValueError("entry must be a single line")
    if text != text.strip():
        raise ValueError("entry must not have leading or trailing whitespace")
    if any(ord(ch) < 0x20 or ord(ch) == 0x7F for ch in text):
        raise ValueError("entry must not contain control characters")
    if len(text) > MAX_CHARS:
        raise ValueError("entry is %d chars, over the 200-char limit" % len(text))
    text.encode("utf-8")
    return text


def main():
    output_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(output_dir, exist_ok=True)
    entry = validate(MESSAGE)
    path = os.path.join(output_dir, "entry.txt")
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(entry)
    # Read back and re-validate what actually landed on disk.
    with open(path, "r", encoding="utf-8") as fh:
        on_disk = validate(fh.read())
    assert on_disk == entry, "entry.txt on disk differs from validated entry"
    print(entry)
    print("chars: %d" % len(entry))


if __name__ == "__main__":
    main()
