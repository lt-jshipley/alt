#!/usr/bin/env python3
"""Stop hook (registered async): the incremental judge.

Builds the turn delta from hook payloads only (last user prompt captured by
UserPromptSubmit + last_assistant_message from Stop) — never parses the
transcript JSONL, whose format is documented as unstable. One stateless
model call updates topics / open loops / corrections in the ledger.

Env:
  CHM_NO_JUDGE=1       skip the model call (counters-only mode)
  CHM_JUDGE_MODEL      model alias for the call (default: haiku)
  CHM_JUDGE_EFFORT     optional --effort level (low|medium|high|xhigh|max)
"""

import json
import os
import subprocess
import sys
import time

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("CHM_JUDGE") == "1":
    sys.exit(0)

import chm_common as chm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JUDGE_PROMPT_PATH = os.path.join(SCRIPT_DIR, "judge_prompt.md")


def call_judge(prompt_text):
    cmd = [
        "claude", "-p",
        "--model", os.environ.get("CHM_JUDGE_MODEL", "haiku"),
        "--settings", '{"disableAllHooks": true}',
        "--strict-mcp-config",
    ]
    effort = os.environ.get("CHM_JUDGE_EFFORT")
    if effort:
        cmd += ["--effort", effort]
    env = dict(os.environ, CHM_JUDGE="1")
    out = subprocess.run(
        cmd, input=prompt_text, capture_output=True, text=True,
        timeout=90, env=env,
    )
    if out.returncode != 0:
        raise RuntimeError(f"judge exit {out.returncode}: {out.stderr[:300]}")
    return out.stdout


def parse_judge_json(raw):
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end <= start:
        raise ValueError(f"no JSON in judge output: {raw[:200]!r}")
    return json.loads(raw[start:end + 1])


payload = chm.read_hook_payload()
if not chm.is_active(payload):
    sys.exit(0)  # not set up for this user or folder: stay inert
if payload.get("stop_hook_active"):
    sys.exit(0)

ledger = chm.resolve_ledger(payload)
sid = ledger["session_id"]
user_prompt = ledger.pop("pending_user_prompt", "")
assistant_msg = chm.get_assistant_message(payload)[:6000]

if not user_prompt and not assistant_msg:
    if payload:
        chm.note_drift(ledger, "last_assistant_message")
    chm.save_ledger(ledger)
    sys.exit(0)

# Raw per-turn stats — recorded, never graded. Material for grading a session
# against the user's own history later.
prompt_ts = ledger.pop("pending_prompt_ts", None)
stat = {"turn": ledger.get("turn", 0), "msg_len": len(assistant_msg)}
if prompt_ts:
    stat["duration_s"] = round(time.time() - prompt_ts)
ledger["turn_stats"] = (ledger.get("turn_stats", []) + [stat])[-50:]

if os.environ.get("CHM_NO_JUDGE") == "1":
    ledger["judge_status"] = "disabled"
    chm.save_ledger(ledger)
    sys.exit(0)

try:
    with open(JUDGE_PROMPT_PATH) as f:
        instructions = f.read()
    open_loops = [l["desc"] for l in ledger["open_loops"]]
    prior_corrections = [e["desc"] for e in ledger.get("correction_log", [])]
    judge_input = (
        f"{instructions}\n\n"
        f"LEDGER:\n{json.dumps({'topics': ledger['topics'], 'open_loops': open_loops, 'prior_corrections': prior_corrections})}\n\n"
        f"TURN DELTA:\nUSER SAID:\n{user_prompt or '(none)'}\n\n"
        f"ASSISTANT REPLIED:\n{assistant_msg or '(none)'}\n"
    )
    verdict = parse_judge_json(call_judge(judge_input))

    chm.record_topics(ledger, verdict.get("topics") or [])
    for desc in (verdict.get("opened_loops") or [])[:5]:
        ledger["open_loops"].append(
            {"desc": str(desc)[:200], "opened_turn": ledger.get("turn", 0)})
    closed = sorted(
        {i for i in (verdict.get("closed_loops") or [])
         if isinstance(i, int) and 0 <= i < len(ledger["open_loops"])},
        reverse=True)
    for i in closed:
        ledger["open_loops"].pop(i)
        ledger["closed_loops"] += 1
    corrections = verdict.get("corrections") or []
    if isinstance(corrections, int):  # pre-repeat judge schema: bare count
        ledger["corrections"] += max(corrections, 0)
    else:
        clog = ledger.get("correction_log", [])
        for item in corrections[:5]:
            if not isinstance(item, dict):
                continue
            rep = item.get("repeat_of")
            if isinstance(rep, int) and 0 <= rep < len(clog):
                clog[rep]["count"] = clog[rep].get("count", 1) + 1
            else:
                clog.append({"desc": str(item.get("desc", ""))[:200], "count": 1})
            ledger["corrections"] += 1
        ledger["correction_log"] = clog[-10:]
    ledger["judge_status"] = "ok"
    ledger["turns_graded"] += 1
except Exception as e:  # a broken judge must never break the session
    ledger["judge_status"] = f"error: {str(e)[:120]}"
    chm.log(f"[{sid[:8]}] judge failed: {e}")

chm.save_ledger(ledger)
