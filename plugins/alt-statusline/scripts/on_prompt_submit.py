#!/usr/bin/env python3
"""UserPromptSubmit hook: capture the prompt for the judge's turn delta, and
inject a health warning into the turn ONLY when the ledger looks anomalous.

Anything printed to stdout on exit 0 becomes context, so this script is
silent unless it is deliberately injecting.
"""

import json
import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("CHM_JUDGE") == "1":
    sys.exit(0)

import chm_common as chm

WARN_COOLDOWN_TURNS = 10

payload = chm.read_hook_payload()
if not chm.is_active(payload):
    sys.exit(0)  # not set up for this user or folder: stay inert
ledger = chm.resolve_ledger(payload)
ledger["turn"] = ledger.get("turn", 0) + 1
ledger["pending_user_prompt"] = chm.get_user_prompt(payload, ledger)[:3000]
ledger["pending_prompt_ts"] = time.time()  # turn duration = submit -> Stop

level, reasons, _flags = chm.grade(ledger, chm.load_ctx(ledger["session_id"]))
recently_warned = ledger["turn"] - ledger.get("last_warned_turn", -999) < WARN_COOLDOWN_TURNS
if level == "restart" and not recently_warned:
    ledger["last_warned_turn"] = ledger["turn"]
    ctx = (
        "[context-health] This session shows signs of context clutter: "
        + "; ".join(reasons)
        + ". Briefly surface this to the user and suggest either explicitly "
        "closing dead ends or restarting from durable artifacts (/clear) at "
        "the next natural boundary. Then answer their prompt normally."
    )
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "UserPromptSubmit",
            "additionalContext": ctx,
        }
    }))

chm.save_ledger(ledger)
