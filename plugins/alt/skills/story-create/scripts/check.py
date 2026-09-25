#!/usr/bin/env python3
"""Deterministic checks on a story-create draft. Prints one line per failure, nothing on a pass."""
import re
import sys

ALLOWED = {"Acceptance criteria", "Examples", "Decided", "Open"}
VOCAB = re.compile(r"\b(runner|sweep|hat|the room)\b", re.I)
TIME = re.compile(r"\b\d{1,2}:\d{2}\b")
HANDLE = re.compile(r"(?<![\w.])@\w+")
PER_NAME = re.compile(r"\bper [A-Z][a-z]+\b")
PAREN_NAME = re.compile(r"\((?:@?[A-Z][a-z]+)(?:,\s*\d{1,2}:\d{2})?\)")
BRACKET = re.compile(r"\[[^\]]+\]")


def main(path):
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()
    fails = []

    # locate title and opener
    body = [l for l in lines]
    idx = 0
    while idx < len(body) and not body[idx].strip():
        idx += 1
    idx += 1  # title line
    while idx < len(body) and not body[idx].strip():
        idx += 1
    opener = []
    while idx < len(body) and body[idx].strip() and not body[idx].startswith("**"):
        opener.append(body[idx].strip())
        idx += 1
    opener_text = " ".join(opener)
    sentences = [s for s in re.split(r"(?<=[.!?])[\"”’)]?\s+", opener_text) if s.strip()]
    if len(sentences) > 4:
        fails.append(f"opener: {len(sentences)} sentences, four allowed")

    # sections
    section = None
    counts = {}
    for n, line in enumerate(lines, 1):
        m = re.match(r"^\*\*(.+?)\*\*\s*$", line.strip())
        if m:
            section = m.group(1).strip()
            if section not in ALLOWED:
                fails.append(f"line {n}: section '{section}' is not in the template")
            counts.setdefault(section, 0)
            continue
        if re.match(r"^(Parent|Waits on|Depends on|Out of scope)\b", line.strip(), re.I):
            fails.append(f"line {n}: '{line.strip()[:40]}' is not in the template")
        if section and re.match(r"^- ", line):
            counts[section] += 1
        if section != "Open" and line.strip():
            if TIME.search(line):
                fails.append(f"line {n}: timestamp outside Open")
            if HANDLE.search(line):
                fails.append(f"line {n}: handle outside Open")
            if PER_NAME.search(line):
                fails.append(f"line {n}: 'per Name' attribution")
            if PAREN_NAME.search(line):
                fails.append(f"line {n}: name in parentheses")
        if BRACKET.search(line) and not re.match(r"^\s*\[?Title", line):
            fails.append(f"line {n}: bracket text left in")
        if "Closed before pickup" in line:
            fails.append(f"line {n}: template instruction copied into the story")
        if VOCAB.search(line):
            fails.append(f"line {n}: skill vocabulary '{VOCAB.search(line).group(0)}'")
    for sec, c in counts.items():
        if c > 3:
            fails.append(f"{sec}: {c} lines, up to three allowed")

    words = len(re.findall(r"\S+", text))
    if words > 600:
        fails.append(f"words: {words}")

    for f in fails:
        print(f)
    return 1 if fails else 0


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("usage: check.py <draft.md>", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(sys.argv[1]))
