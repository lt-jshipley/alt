#!/usr/bin/env python3
"""Pure event-identity counter: `on_counter.py <counter_name>`.

Which counter to increment comes from argv at registration time — the hook
FIRING is the fact. Stdin is read only to key the session ledger; an empty
or reshaped payload still counts correctly (against the 'current' ledger).
Inert until setup.py has installed the monitor (chm.is_active). Parallel
tool calls fire this concurrently; locked_ledger keeps every increment.

Registered as:
  PostToolUse        -> on_counter.py tool_calls
  PostToolUseFailure -> on_counter.py tool_failures
"""

import os
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("CHM_JUDGE") == "1":
    sys.exit(0)  # never run inside our own judge subprocess

import chm_common as chm

VALID = {"tool_calls", "tool_failures", "compactions"}
counter = sys.argv[1] if len(sys.argv) > 1 else ""
if counter not in VALID:
    chm.log(f"on_counter: bad counter arg {counter!r}")
    sys.exit(0)

payload = chm.read_hook_payload()
if not chm.is_active():
    sys.exit(0)  # not set up: stay inert

with chm.locked_ledger(payload) as ledger:
    ledger["counters"][counter] += 1
    if counter == "tool_failures":
        # streak + timestamps feed the clustering signal in grade(); still pure
        # event identity — wall clock, not payload
        ledger["fail_streak"] = ledger.get("fail_streak", 0) + 1
        ledger["fail_times"] = (ledger.get("fail_times", []) + [time.time()])[-10:]
        err = chm.get_error(payload).splitlines()
        if err:
            chm.log(f"[{ledger['session_id'][:8]}] FAIL "
                    f"{payload.get('tool_name', '?')}: {err[0][:160]}")
    elif counter == "tool_calls":
        ledger["fail_streak"] = 0  # any success ends the streak
