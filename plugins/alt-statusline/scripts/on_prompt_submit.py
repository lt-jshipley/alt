#!/usr/bin/env python3
"""UserPromptSubmit hook: stamp the turn, queue the prompt for the judge's
turn delta, and inject a health warning into the turn once per red episode.

Anything printed to stdout on exit 0 becomes context, so this script is
silent unless it is deliberately injecting — and it prints only after the
ledger lock is released.
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("CHM_JUDGE") == "1":
    sys.exit(0)

import chm_common as chm

payload = chm.read_hook_payload()
if not chm.is_active():
    sys.exit(0)  # not set up: stay inert

injection = None
with chm.locked_ledger(payload) as ledger:
    ledger["turn"] = ledger.get("turn", 0) + 1
    # Queued, not a single slot: the async Stop for the previous turn may
    # still be running and consumes by timestamp (see on_stop.py).
    pending = ledger.get("pending_prompts") or []
    pending.append({
        "turn": ledger["turn"],
        "prompt": chm.get_user_prompt(payload, ledger)[:3000],
        "ts": time.time(),  # turn duration = submit -> Stop
    })
    ledger["pending_prompts"] = pending[-chm.PENDING_PROMPTS_CAP:]

    level, reasons, _flags = chm.grade(ledger, chm.load_ctx(ledger["session_id"]))
    # One nudge per red episode; the label carries it from then on. Re-armed
    # when the grade drops below red (loops close, context shrinks). Compaction
    # and a 3x-repeated correction never drop, so those warn once per session.
    if level == "restart":
        if not ledger.get("warned_red"):
            ledger["warned_red"] = True
            injection = (
                "[context-health] This session shows signs of context clutter: "
                + "; ".join(reasons)
                + ". Briefly surface this to the user and suggest either explicitly "
                "closing dead ends or restarting from durable artifacts (/clear) at "
                "the next natural boundary. Then answer their prompt normally."
            )
    else:
        ledger["warned_red"] = False

if injection:
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": injection,
        }
    }))
