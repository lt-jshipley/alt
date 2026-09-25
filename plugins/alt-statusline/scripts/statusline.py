#!/usr/bin/env python3
"""Custom statusline: identity/environment row (model · effort | git
segment), the gauge row (drift grade, context %, health chips), and a topics
row (per-session mention counts, once the judge has tagged any). The red
tier's label is itself the call to action: "Restart Recommended".
Receives session JSON on stdin; re-runs after every assistant message.
Computes nothing semantic — just displays the ledger. With no ledger for this
session (hooks not yet fired, or the monitor not set up) it
renders identity + git and a dim "Session: no data".

Installed via setup.py, which points the statusLine setting at a stable
launcher in the state dir; the launcher runs this file from the plugin root
the session started with (stamped in its ledger), falling back to the
registry's root.

Grading lives in chm_common.grade() — shared with on_prompt_submit so the
statusline band and the injected warning can never disagree.
"""

import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chm_common as chm

GREEN, YELLOW, RED = "\033[32m", "\033[33m", "\033[31m"
CYAN, MAGENTA, DIM, RESET = "\033[36m", "\033[35m", "\033[2m", "\033[0m"
ORANGE = "\033[38;5;208m"  # 256-color; the moderate tier between yellow and red

LEVELS = {
    "stable": (GREEN, "Stable"),
    "minor": (YELLOW, "Drifting"),
    "moderate": (ORANGE, "Degrading"),
    "restart": (RED, "Restart Recommended"),
}


GIT_CACHE_TTL = 5  # seconds — this statusline re-renders every assistant
                   # message, far hotter than a shell prompt. Cached per
                   # session so concurrent sessions in different repos don't
                   # thrash one file.

CONFLICT_XY = {"UU", "AA", "DD", "AU", "UA", "DU", "UD"}
IN_PROGRESS = [  # first match wins; markers live in the PER-WORKTREE git dir
    ("rebase-merge", "REBASING"),
    ("rebase-apply", "REBASING"),
    ("MERGE_HEAD", "MERGING"),
    ("CHERRY_PICK_HEAD", "CHERRY-PICKING"),
    ("REVERT_HEAD", "REVERTING"),
    ("BISECT_LOG", "BISECTING"),
]


def build_git_segment(d):
    """dir · branch with supervision states: +staged !unstaged ?untracked
    =conflicts, in-progress op labels, DETACHED, ⚠ default branch, ⎇wt
    linked worktree, ↑ahead ↓behind. Red = conflicts/op/⚠/detached,
    yellow = dirty, green = clean."""

    def git(*args):
        try:
            r = subprocess.run(["git", "-C", d, *args],
                               capture_output=True, text=True, timeout=2)
            return r.stdout.strip() if r.returncode == 0 else ""
        except (OSError, subprocess.TimeoutExpired):
            return ""

    seg = f"{CYAN}{os.path.basename(d)}{RESET}"
    branch = git("branch", "--show-current")
    detached = False
    if not branch:
        sha = git("rev-parse", "--short", "HEAD")
        if not sha:
            return seg  # not a repo
        branch, detached = f"@{sha}", True

    staged = unstaged = untracked = conflicts = 0
    for line in git("status", "--porcelain").splitlines():
        if len(line) < 2:
            continue
        xy = line[:2]
        if xy == "??":
            untracked += 1
        elif xy in CONFLICT_XY:
            conflicts += 1
        else:
            if xy[0] not in " ?!":
                staged += 1
            if xy[1] not in " ?":
                unstaged += 1

    # per-worktree git dir: in-progress markers live here, and differing from
    # the common dir IS the linked-worktree indicator — one call covers both
    op = worktree = ""
    dirs = git("rev-parse", "--git-dir", "--git-common-dir").splitlines()
    if len(dirs) == 2:
        gd, cd = (p if os.path.isabs(p) else os.path.join(d, p) for p in dirs)
        for marker, label in IN_PROGRESS:
            if os.path.exists(os.path.join(gd, marker)):
                op = label
                break
        if os.path.realpath(gd) != os.path.realpath(cd):
            worktree = "⎇wt"

    defaults = os.environ.get("CHM_DEFAULT_BRANCH", "main,master")
    warn = not detached and branch in [b.strip() for b in defaults.split(",")]

    dirty = staged + unstaged + untracked
    color = (RED if (conflicts or op or warn or detached)
             else YELLOW if dirty else GREEN)

    marks = []
    if op:
        marks.append(op)
    if conflicts:
        marks.append(f"={conflicts}")
    if staged:
        marks.append(f"+{staged}")
    if unstaged:
        marks.append(f"!{unstaged}")
    if untracked:
        marks.append(f"?{untracked}")
    if worktree:
        marks.append(worktree)
    counts = git("rev-list", "--left-right", "--count", "@{upstream}...HEAD")
    if counts:
        behind, ahead = (counts.split() + ["0", "0"])[:2]
        if ahead.isdigit() and int(ahead) > 0:
            marks.append(f"↑{ahead}")
        if behind.isdigit() and int(behind) > 0:
            marks.append(f"↓{behind}")

    label = ("DETACHED " if detached else "⚠ " if warn else "") + branch
    tail = (" " + " ".join(marks)) if marks else ""
    return f"{seg} {color}{label}{tail}{RESET}"


def git_segment(d, cache_path):
    """TTL-cached wrapper around build_git_segment — the cached string
    carries every state, so one cache covers all the checks."""
    if not d:
        return ""
    now = time.time()
    try:
        with open(cache_path) as f:
            c = json.load(f)
        if c.get("dir") == d and now - c.get("ts", 0) < GIT_CACHE_TTL:
            return c.get("text", "")
    except (OSError, json.JSONDecodeError, ValueError):
        pass
    text = build_git_segment(d)
    chm.atomic_write(cache_path, {"dir": d, "ts": now, "text": text})
    return text


try:
    data = json.load(sys.stdin)
except (json.JSONDecodeError, OSError):
    data = {}

sid = data.get("session_id", "")
# No fallback to the shared 'current' ledger here: showing another session's
# grade is worse than "no data". Hooks keep that fallback so counting never
# stops; only the display refuses to borrow.
has_ledger = bool(sid) and os.path.exists(chm.ledger_path(sid))
git_cache = (os.path.join(chm.SESSIONS_DIR, f"{sid}.git.json") if sid
             else os.path.join(chm.STATE_DIR, "gitseg.json"))

cw = data.get("context_window") or {}
pct = cw.get("used_percentage")
# live context size = input + cache_creation + cache_read; the docs publish
# that sum as total_input_tokens and break it out under current_usage (an
# object, never a number)
tokens = cw.get("total_input_tokens")
if not tokens and isinstance(cw.get("current_usage"), dict):
    u = cw["current_usage"]
    tokens = sum(u.get(k) or 0 for k in
                 ("input_tokens", "cache_creation_input_tokens", "cache_read_input_tokens"))
model = (data.get("model") or {}).get("display_name", "")
effort = (data.get("effort") or {}).get("level", "")
workdir = (data.get("workspace") or {}).get("current_dir") or data.get("cwd", "")

line1, line2 = [], []

if model:
    line1.append(f"{MAGENTA}{model}{' · ' + effort if effort else ''}{RESET}")
gs = git_segment(workdir, git_cache)
if gs:
    line1.append(gs)

level, flags = "stable", set()
led = chm.load_ledger(sid) if has_ledger else None
if led:
    if pct is not None or tokens:
        chm.save_ctx(sid, pct, tokens)  # grading sidecar; ledger untouched
    level, _reasons, flags = chm.grade(led, chm.load_ctx(sid))
    color, label = LEVELS[level]
    line2.append(f"Session: {color}{label}{RESET}")
else:
    line2.append(f"{DIM}Session: no data{RESET}")

band = LEVELS[level][0]

if pct is not None:
    # a context flag paints the % chip in the band color; display bands
    # otherwise match the grading thresholds (25/40)
    pc = band if "context" in flags else (
        RED if pct >= chm.RED_CTX_PCT else
        YELLOW if pct >= chm.ELEV_CTX_PCT else GREEN)
    tok = ""
    if isinstance(tokens, (int, float)) and tokens > 0:
        tok = (f" ({tokens / 1e6:.1f}M)" if tokens >= 1e6
               else f" ({tokens / 1e3:.0f}k)" if tokens >= 1000
               else f" ({int(tokens)})")
    line2.append(f"{pc}{round(pct)}% used{tok}{RESET}")

if led:
    c = led["counters"]

    def chip(text, key):
        # culprit chips wear the band color; healthy chips are green
        return f"{band}{text}{RESET}" if key in flags else f"{GREEN}{text}{RESET}"

    # loose ends: approaches or questions the session started and never
    # said it finished; resolved concepts: the ones it did. Separate chips,
    # never a fraction: 5 loose ends beside 4 resolved is a normal reading.
    # ai misunderstandings: the times the user redirected the assistant away
    # from something it did or misread. Always shown, like its neighbours.
    health = [
        chip(f"topics:{len(led['topics'])}", "topics"),
        chip(f"resolved concepts:{led['closed_loops']}", "loops"),
        chip(f"loose ends:{len(led['open_loops'])}", "loops"),
        chip(f"ai misunderstandings:{led['corrections']}", "corrections"),
        chip(f"cli tool fails:{c['tool_failures']}/{c['tool_calls'] + c['tool_failures']}", "fails"),
    ]
    if c["compactions"]:
        health.append(chip(f"compactions:{c['compactions']}", "compactions"))
    status = str(led.get("judge_status", "pending"))
    if status != "ok":
        health.append(chip(f"judge:{status.split(':')[0]}", "infra"))
    if led.get("schema_drift"):
        health.append(chip("⚠ drift:" + ",".join(led["schema_drift"]), "infra"))
    line2.append(" · ".join(health))

if line1:  # degraded stdin may leave no model/git — never a blank top row
    print(" | ".join(line1))
print(" | ".join(line2))

# line 3: session topics with per-session mention counts, busiest first —
# rendered only when the judge has tagged anything. Unstyled on purpose: it
# inherits the theme's default foreground (ANSI dim is unreadably low-contrast
# on some themes).
if led and led["topics"]:
    counts = led.get("topic_counts", {})
    ranked = sorted(led["topics"], key=lambda t: -counts.get(t, 0))[:6]
    tc = " | ".join(
        f"{t}:{counts[t]}" if counts.get(t) else t for t in ranked)
    print(f"Topics: {tc}")
