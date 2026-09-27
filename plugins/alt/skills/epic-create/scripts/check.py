#!/usr/bin/env python3
"""Deterministic checks on an epic-create draft. Prints one line per failure, nothing on a pass.

usage: check.py <draft.md> [seed.md]
With a seed, every digit sequence in the draft must also appear in the seed.
"""
import re
import sys

ALLOWED = {"Bet", "Decided", "Open"}
VOCAB = re.compile(r"\b(runner|sweep|hat|the room)\b", re.I)
TIME = re.compile(r"\b\d{1,2}:\d{2}\b")
HANDLE = re.compile(r"(?<![\w.])@\w+")
OMIT = re.compile(r"\b(left out|stays? out|out of this epic|not in this epic|unrelated)\b", re.I)
PAREN_NAME = re.compile(r"\((?:@?[A-Z][a-z]+)(?:,\s*\d{1,2}:\d{2})?\)")
BRACKET = re.compile(r"\[[^\]]+\]")
CONFIDENCE = re.compile(r"\bconfidence\b", re.I)
FORBIDDEN_LINE = re.compile(
    r"^(Parent|Holds|Not yet a story|Not:|Depends on|Out of scope|Conditions|Acceptance|Stories|Children|Target:|Due)\b",
    re.I,
)
OUTCOME = re.compile(r"^\*\*Outcome:\*\*")
NUMBER = re.compile(r"\d+")


def main(path, seed_path=None):
    text = open(path, encoding="utf-8").read()
    lines = text.splitlines()
    fails = []

    # locate title and opener
    idx = 0
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    idx += 1  # title line
    while idx < len(lines) and not lines[idx].strip():
        idx += 1
    opener = []
    while idx < len(lines) and lines[idx].strip() and not lines[idx].startswith("**"):
        opener.append(lines[idx].strip())
        idx += 1
    opener_text = " ".join(opener)
    sentences = [s for s in re.split(r"(?<=[.!?])[\"”’)]?\s+", opener_text) if s.strip()]
    if len(sentences) > 3:
        fails.append(f"opener: {len(sentences)} sentences, three allowed")

    outcomes = sum(1 for l in lines if OUTCOME.match(l.strip()))
    if outcomes != 1:
        fails.append(f"outcome: {outcomes} lines, one required")

    section = None
    counts = {}
    for n, line in enumerate(lines, 1):
        stripped = line.strip()
        m = re.match(r"^\*\*(.+?)\*\*\s*$", stripped)
        if m:
            section = m.group(1).strip()
            if section not in ALLOWED:
                fails.append(f"line {n}: section '{section}' is not in the template")
            counts.setdefault(section, 0)
            continue
        if FORBIDDEN_LINE.match(stripped) or FORBIDDEN_LINE.match(stripped.strip("*")):
            fails.append(f"line {n}: '{stripped[:40]}' is not in the template")
        if section and re.match(r"^- ", line):
            counts[section] += 1
        if section != "Open" and stripped:
            if TIME.search(line):
                fails.append(f"line {n}: timestamp outside Open")
            if HANDLE.search(line):
                fails.append(f"line {n}: handle outside Open")
            if PAREN_NAME.search(line):
                fails.append(f"line {n}: name in parentheses")
        if section == "Decided" and OMIT.search(line):
            fails.append(f"line {n}: Decided records what the epic leaves out")
        if BRACKET.search(line) and not re.match(r"^\s*\[?Title", line):
            fails.append(f"line {n}: bracket text left in")
        if "Closed before pickup" in line or "changes only what gets built" in line:
            fails.append(f"line {n}: template instruction copied into the epic")
        if CONFIDENCE.search(line):
            fails.append(f"line {n}: confidence word")
        if VOCAB.search(line):
            fails.append(f"line {n}: skill vocabulary '{VOCAB.search(line).group(0)}'")
    for sec, c in counts.items():
        if c > 3:
            fails.append(f"{sec}: {c} lines, up to three allowed")

    if seed_path:
        seed = open(seed_path, encoding="utf-8").read()
        seed_numbers = set(NUMBER.findall(seed))
        for n, line in enumerate(lines, 1):
            for num in NUMBER.findall(line):
                if num not in seed_numbers:
                    fails.append(f"line {n}: number {num} is not in the seed")

    words = len(re.findall(r"\S+", text))
    if words > 350:
        fails.append(f"words: {words}")

    for f in fails:
        print(f)
    return 1 if fails else 0


if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        print("usage: check.py <draft.md> [seed.md]", file=sys.stderr)
        sys.exit(2)
    sys.exit(main(*sys.argv[1:]))
