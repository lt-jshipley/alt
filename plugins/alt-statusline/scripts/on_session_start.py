#!/usr/bin/env python3
"""SessionStart hook, arg-driven: `on_session_start.py <compact|fresh>`.

The SessionStart MATCHER decides which mode runs — the payload's `source`
field is never read (event identity over payload shape).

compact: fires after compaction. Counts the splice and re-injects the ledger
losslessly via stdout (plain stdout on exit 0 becomes context), so the
monitor's state survives the summary. A Stop still grading when compaction
fires is one cycle behind; its loops appear on the next turn's ledger, not in
this injection.

fresh: fires on startup|resume|clear|fork. Loads (never resets) the session
ledger, runs the environment canary (claude on PATH unless CHM_NO_JUDGE=1,
judge prompt readable, state writable), and refreshes the registry's
plugin_root from CLAUDE_PLUGIN_ROOT (the launcher's fallback root).
Prints NOTHING — stdout would be injected into the session.

Both modes stamp CLAUDE_PLUGIN_ROOT into the ledger as plugin_root, so the
launcher renders this session with the plugin version it started with.
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
if mode not in ("compact", "fresh"):
    chm.log(f"on_session_start: bad mode arg {mode!r}")
    sys.exit(0)

payload = chm.read_hook_payload()
if not chm.is_active():
    sys.exit(0)  # not set up: stay inert

root = os.environ.get("CLAUDE_PLUGIN_ROOT")

if mode == "compact":
    with chm.locked_ledger(payload) as ledger:
        if root:
            ledger["plugin_root"] = root
        ledger["counters"]["compactions"] += 1
        loops = "; ".join(l["desc"] for l in ledger["open_loops"]) or "none"
        topics = ", ".join(ledger["topics"]) or "none"
        c = dict(ledger["counters"])
    print(  # after the lock is released
        "[context-health] State restored across compaction (lossless, from "
        f"the session ledger): topics so far: {topics}. Open loops still "
        f"unresolved: {loops}. Tool failures this session: "
        f"{c['tool_failures']} (compaction #{c['compactions']}). Treat every "
        "open loop above as unresolved unless it was explicitly closed."
    )
else:
    if root:
        seen = {}

        def _refresh(reg):
            seen["was"] = reg.get("plugin_root")
            reg["plugin_root"] = root

        try:
            chm.update_registry(_refresh)
            if seen.get("was") != root:
                chm.log(f"plugin_root refreshed: {root}")
        except OSError as e:
            chm.log(f"registry refresh failed: {e}")
    problems = []
    if os.environ.get("CHM_NO_JUDGE") != "1" and not shutil.which("claude"):
        problems.append("claude not on PATH")  # counters-only mode needs no judge
    if not os.access(os.path.join(SCRIPT_DIR, "judge_prompt.md"), os.R_OK):
        problems.append("judge_prompt.md unreadable")
    try:
        os.makedirs(chm.SESSIONS_DIR, exist_ok=True)
    except OSError:
        pass
    if not os.access(chm.SESSIONS_DIR, os.W_OK):
        problems.append("state dir not writable")
    with chm.locked_ledger(payload) as ledger:
        if root:
            ledger["plugin_root"] = root
        if problems:
            ledger["judge_status"] = f"error: canary: {'; '.join(problems)}"[:150]
            chm.log(f"[{ledger['session_id'][:8]}] canary FAILED: {problems}")
        else:
            if str(ledger.get("judge_status", "")).startswith("error: canary"):
                ledger["judge_status"] = "pending"  # environment fixed since
            chm.log(f"[{ledger['session_id'][:8]}] session start, canary ok")
