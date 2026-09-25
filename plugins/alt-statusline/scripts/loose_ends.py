#!/usr/bin/env python3
"""Loose ends: list and close the session's open loops by hand.

    loose_ends.py list  [--session ID]
    loose_ends.py close <n> [<n>...] | --all  [--session ID]

A loose end is an approach or question the judge saw the session start and
never saw it finish. The judge closes one only when a later turn says so in
words, and it runs a cycle behind, so the session model, which knows the
conversation better than the judge does, can close them here on the user's
say-so. Closing is a ledger write, not a hint to the judge.

The session comes from CLAUDE_CODE_SESSION_ID, which Claude Code exports to
commands run inside a session; --session overrides it. Numbers refer to the
order `list` printed, oldest first, and are checked against the live list.

Locks: close takes the judge lock first, then the ledger lock, the same order
as the Stop hook, so it never interleaves with a verdict being applied by
index. If the judge is still grading after CHM_JUDGE_WAIT_S it says so and
writes nothing; nothing here may block the session.
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import chm_common as chm

JUDGE_WAIT_S = chm.env_float("CHM_JUDGE_WAIT_S", 25.0)
USAGE = "usage: loose_ends.py list | close <n> [<n>...] | close --all  [--session ID]"


def session_from(args):
    if "--session" in args:
        i = args.index("--session")
        if i + 1 >= len(args):
            return None, args
        sid = args[i + 1]
        return sid, args[:i] + args[i + 2:]
    return os.environ.get("CLAUDE_CODE_SESSION_ID"), args


def valid_sid(sid):
    return isinstance(sid, str) and sid and "/" not in sid and sid not in (".", "..")


def age_word(ledger, loop):
    age = ledger.get("turn", 0) - loop.get("opened_turn", 0)
    turns = f"{age} turn" + ("" if age == 1 else "s")
    stale = loop in chm.stale_open_loops(ledger)
    return f"open {turns}" + (", counts against the session" if stale else "")


def cmd_list(sid):
    if not os.path.exists(chm.ledger_path(sid)):
        print("no ledger for this session yet; the gauge has not seen a turn")
        return 0
    ledger = chm.load_ledger(sid)
    loops = ledger["open_loops"]
    if not loops:
        print(f"no loose ends. resolved this session: {ledger['closed_loops']}")
        return 0
    for n, loop in enumerate(loops, 1):
        print(f"{n}. {loop.get('desc', '')}  ({age_word(ledger, loop)})")
    print(f"resolved this session: {ledger['closed_loops']}")
    return 0


def cmd_close(sid, args):
    if not args:
        print(USAGE)
        return 2
    close_all = args == ["--all"]
    if not close_all:
        try:
            wanted = sorted({int(a) for a in args})
        except ValueError:
            print(USAGE)
            return 2
        if any(n < 1 for n in wanted):
            print(USAGE)
            return 2
    if not os.path.exists(chm.ledger_path(sid)):
        print("no ledger for this session yet; nothing to close")
        return 0
    with chm.judge_lock(sid, JUDGE_WAIT_S) as acquired:
        if not acquired:
            print("the judge is still grading the last turn; try again in a moment. nothing closed")
            return 0
        with chm.locked_ledger({"session_id": sid}) as ledger:
            loops = ledger["open_loops"]
            if close_all:
                wanted = list(range(1, len(loops) + 1))
            missing = [n for n in wanted if n > len(loops)]
            if missing:
                print(f"no loose end numbered {', '.join(map(str, missing))}; "
                      f"the list holds {len(loops)}. nothing closed")
                return 0
            closed = []
            for n in sorted(wanted, reverse=True):
                closed.append(loops.pop(n - 1).get("desc", ""))
                ledger["closed_loops"] += 1
            left = len(loops)
            resolved = ledger["closed_loops"]
    for desc in reversed(closed):
        print(f"closed: {desc}")
    print(f"loose ends left: {left}. resolved this session: {resolved}")
    return 0


def main(argv):
    sid, args = session_from(argv)
    if not args:
        print(USAGE)
        return 2
    if not chm.is_active():
        print("alt-statusline is not installed; run /alt-statusline:setup")
        return 0
    if not valid_sid(sid):
        print("no session id: CLAUDE_CODE_SESSION_ID is unset and --session was not given")
        return 0
    cmd, rest = args[0], args[1:]
    if cmd == "list" and not rest:
        return cmd_list(sid)
    if cmd == "close":
        return cmd_close(sid, rest)
    print(USAGE)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
