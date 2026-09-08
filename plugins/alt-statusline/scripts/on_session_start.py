#!/usr/bin/env python3
"""SessionStart hook, arg-driven: `on_session_start.py <compact|fresh>`.

The SessionStart MATCHER decides which mode runs — the payload's `source`
field is never read (event identity over payload shape).

compact: fires after compaction. Counts the splice and re-injects the ledger
losslessly via stdout (plain stdout on exit 0 becomes context), so the
monitor's state survives the summary.

fresh: fires on startup|resume|clear|fork. Loads (never resets) the session
ledger, runs the environment canary (claude on PATH, judge prompt readable,
state writable), and refreshes the registry's plugin_root from
CLAUDE_PLUGIN_ROOT so the statusline launcher follows plugin updates.
Prints NOTHING — stdout would be injected into the session.
"""

import os
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("CHM_JUDGE") == "1":
    sys.exit(0)

import chm_common as chm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
mode = sys.argv[1] if len(sys.argv) > 1 else ""

payload = chm.read_hook_payload()
if not chm.is_active(payload):
    sys.exit(0)  # not set up for this user or folder: stay inert
ledger = chm.resolve_ledger(payload)

if mode == "compact":
    ledger["counters"]["compactions"] += 1
    chm.save_ledger(ledger)
    loops = "; ".join(l["desc"] for l in ledger["open_loops"]) or "none"
    topics = ", ".join(ledger["topics"]) or "none"
    c = ledger["counters"]
    print(
        "[context-health] State restored across compaction (lossless, from "
        f"the session ledger): topics so far: {topics}. Open loops still "
        f"unresolved: {loops}. Tool failures this session: "
        f"{c['tool_failures']} (compaction #{c['compactions']}). Treat every "
        "open loop above as unresolved unless it was explicitly closed."
    )
elif mode == "fresh":
    root = os.environ.get("CLAUDE_PLUGIN_ROOT")
    if root:
        reg = chm.load_registry()
        if reg.get("plugin_root") != root:
            reg["plugin_root"] = root
            chm.save_registry(reg)
            chm.log(f"plugin_root refreshed: {root}")
    problems = []
    if not shutil.which("claude"):
        problems.append("claude not on PATH")
    if not os.access(os.path.join(SCRIPT_DIR, "judge_prompt.md"), os.R_OK):
        problems.append("judge_prompt.md unreadable")
    try:
        os.makedirs(chm.SESSIONS_DIR, exist_ok=True)
    except OSError:
        pass
    if not os.access(chm.SESSIONS_DIR, os.W_OK):
        problems.append("state dir not writable")
    if problems:
        ledger["judge_status"] = f"error: canary: {'; '.join(problems)}"[:150]
        chm.log(f"[{ledger['session_id'][:8]}] canary FAILED: {problems}")
    else:
        chm.log(f"[{ledger['session_id'][:8]}] session start, canary ok")
    chm.save_ledger(ledger)
else:
    chm.log(f"on_session_start: bad mode arg {mode!r}")
