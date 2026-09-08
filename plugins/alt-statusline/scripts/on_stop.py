#!/usr/bin/env python3
"""Stop hook (registered async): the incremental judge.

Builds the turn delta from hook payloads only (the prompt queued by
UserPromptSubmit + last_assistant_message from Stop) — never parses the
transcript JSONL, whose format is documented as unstable. One stateless
model call updates topics / open loops / corrections in the ledger. The
judge's instructions travel as its system prompt (--system-prompt-file) and
it runs from the state dir, so no project CLAUDE.md, rules, or MCP config
reach it; only the user-level ~/.claude/CLAUDE.md still loads.

Concurrency. This hook runs while the next turn is already underway, and a
fast next turn can start a second Stop before this one's judge returns, so:
  Phase A1  (ledger lock, ms)  consume the prompt, record turn stats
  judge lock                   serialize Stops per session; skip if busy
  Phase A2  (ledger lock, ms)  snapshot the judge's input
  judge     (no locks, <=90s)  the model call
  Phase B   (ledger lock, ms)  reload and apply the verdict by index
Only Stops write the judge-owned fields, and Stops are serialized, so the
snapshot is exactly what Phase B sees and the judge's indices stay valid.

Prompt attribution. pending_prompts is a queue, consumed by timestamp: a
prompt stamped within PROMPT_SETTLE_S of this process starting is the NEXT
turn's (queued input whose UserPromptSubmit won the startup race) and is left
alone; among older entries the newest is ours and any before it belong to
interrupted turns (Stop never fired) and are dropped with a log line.

Env:
  CHM_NO_JUDGE=1       skip the model call (counters-only mode)
  CHM_JUDGE_MODEL      model alias for the call (default: haiku)
  CHM_JUDGE_EFFORT     optional --effort level (low|medium|high|xhigh|max)
  CHM_JUDGE_WAIT_S     seconds to wait for a running judge (default 25)
"""

import json
import os
import subprocess
import sys
import time

T0 = time.time()  # before anything else: prompt attribution keys off it

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
if os.environ.get("CHM_JUDGE") == "1":
    sys.exit(0)

import chm_common as chm

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
JUDGE_PROMPT_PATH = os.path.join(SCRIPT_DIR, "judge_prompt.md")
JUDGE_TIMEOUT_S = 90
STOP_BUDGET_S = 110         # hooks.json allows 120; keep 10 for the phases
PROMPT_SETTLE_S = 1.0
JUDGE_WAIT_S = chm.env_float("CHM_JUDGE_WAIT_S", 25.0)


def call_judge(delta_text, timeout):
    """One-shot `claude -p`: instructions as the system prompt, the delta on
    stdin, run from the state dir so nothing project-level is loaded."""
    if not os.access(JUDGE_PROMPT_PATH, os.R_OK):
        raise RuntimeError(f"judge prompt unreadable: {JUDGE_PROMPT_PATH}")
    cmd = [
        "claude", "-p",
        "--model", os.environ.get("CHM_JUDGE_MODEL", "haiku"),
        "--system-prompt-file", JUDGE_PROMPT_PATH,  # replaces the built-in prompt
        "--settings", '{"disableAllHooks": true}',
        "--strict-mcp-config",
        "--no-session-persistence",   # no transcript per turn under ~/.claude/projects
        "--tools", "",                # the judge reads a document; it needs no tools
    ]
    effort = os.environ.get("CHM_JUDGE_EFFORT")
    if effort:
        cmd += ["--effort", effort]
    env = dict(os.environ, CHM_JUDGE="1")
    out = subprocess.run(
        cmd, input=delta_text, capture_output=True, text=True,
        timeout=timeout, env=env, cwd=chm.STATE_DIR,
    )
    if out.returncode != 0:
        raise RuntimeError(f"judge exit {out.returncode}: {out.stderr[:300]}")
    return out.stdout


def parse_judge_json(raw):
    start, end = raw.find("{"), raw.rfind("}")
    if start == -1 or end <= start:
        raise ValueError(f"no JSON in judge output: {raw[:200]!r}")
    return json.loads(raw[start:end + 1])


def consume_prompt(ledger):
    """Phase A1: pop the prompt this Stop closes out (see module docstring)."""
    pending = ledger.get("pending_prompts") or []
    cutoff = T0 - PROMPT_SETTLE_S
    ours = [p for p in pending if p.get("ts", 0) < cutoff]
    ledger["pending_prompts"] = [p for p in pending if p.get("ts", 0) >= cutoff]
    for orphan in ours[:-1]:
        chm.log(f"[{ledger['session_id'][:8]}] dropping unconsumed prompt from "
                f"turn {orphan.get('turn')} (interrupted turn?)")
    return ours[-1] if ours else None


def _is_index(i, n):
    return isinstance(i, int) and not isinstance(i, bool) and 0 <= i < n


def apply_verdict(ledger, verdict, turn, n_loops, n_corr):
    """Phase B. Indices refer to the Phase A2 snapshot, which — Stops being
    serialized — is the first n_loops / n_corr entries of the fresh lists.
    Close before opening so an index can never hit a loop opened by this
    same verdict."""
    chm.record_topics(ledger, verdict.get("topics") or [])
    closed = sorted({i for i in (verdict.get("closed_loops") or [])
                     if _is_index(i, n_loops)}, reverse=True)
    for i in closed:
        if i < len(ledger["open_loops"]):
            ledger["open_loops"].pop(i)
            ledger["closed_loops"] += 1
    for desc in (verdict.get("opened_loops") or [])[:5]:
        ledger["open_loops"].append({"desc": str(desc)[:200], "opened_turn": turn})
    corrections = verdict.get("corrections") or []
    if isinstance(corrections, int) and not isinstance(corrections, bool):
        ledger["corrections"] += max(corrections, 0)  # pre-repeat judge schema
    else:
        clog = ledger.get("correction_log", [])
        for item in list(corrections)[:5]:
            if not isinstance(item, dict):
                continue
            rep = item.get("repeat_of")
            if _is_index(rep, n_corr) and rep < len(clog):
                clog[rep]["count"] = clog[rep].get("count", 1) + 1
            else:
                clog.append({"desc": str(item.get("desc", ""))[:200], "count": 1})
            ledger["corrections"] += 1
        ledger["correction_log"] = clog[-10:]


payload = chm.read_hook_payload()
if not chm.is_active():
    sys.exit(0)  # not set up: stay inert
if payload.get("stop_hook_active"):
    sys.exit(0)

raw_msg = chm.get_assistant_message(payload)
assistant_msg = chm.clip_middle(raw_msg)  # head + tail: conclusions survive

# --- Phase A1 --------------------------------------------------------------
proceed = False
with chm.locked_ledger(payload) as ledger:
    sid = ledger["session_id"]
    entry = consume_prompt(ledger) or {}
    user_prompt = entry.get("prompt", "")
    turn = entry.get("turn", ledger.get("turn", 0))
    if not user_prompt and not assistant_msg:
        if payload:
            chm.note_drift(ledger, "last_assistant_message")
    else:
        # Raw per-turn stats — recorded, never graded. Material for grading a
        # session against the user's own history later.
        stat = {"turn": turn, "msg_len": len(raw_msg)}
        if entry.get("ts"):
            stat["duration_s"] = round(T0 - entry["ts"])
        ledger["turn_stats"] = (ledger.get("turn_stats", []) + [stat])[-50:]
        if os.environ.get("CHM_NO_JUDGE") == "1":
            ledger["judge_status"] = "disabled"
        else:
            proceed = True
if not proceed:
    sys.exit(0)

# --- judge lock, Phase A2, judge, Phase B -----------------------------------
with chm.judge_lock(sid, JUDGE_WAIT_S) as acquired:
    if not acquired:
        with chm.locked_ledger(payload) as ledger:
            ledger["judge_status"] = "skipped: busy"
        chm.log(f"[{sid[:8]}] judge still running after {JUDGE_WAIT_S:g}s; "
                f"turn {turn} not graded")
        sys.exit(0)

    with chm.locked_ledger(payload) as ledger:
        snapshot = {
            "topics": list(ledger["topics"]),
            "open_loops": [l["desc"] for l in ledger["open_loops"]],
            "prior_corrections": [e["desc"] for e in ledger.get("correction_log", [])],
        }
    n_loops, n_corr = len(snapshot["open_loops"]), len(snapshot["prior_corrections"])

    try:
        judge_input = (  # the instructions ride along as the system prompt
            f"LEDGER:\n{json.dumps(snapshot)}\n\n"
            f"TURN DELTA:\nUSER SAID:\n{user_prompt or '(none)'}\n\n"
            f"ASSISTANT REPLIED:\n{assistant_msg or '(none)'}\n"
        )
        remaining = STOP_BUDGET_S - (time.time() - T0)
        verdict = parse_judge_json(
            call_judge(judge_input, timeout=max(5, min(JUDGE_TIMEOUT_S, remaining))))
        with chm.locked_ledger(payload) as ledger:
            apply_verdict(ledger, verdict, turn, n_loops, n_corr)
            ledger["judge_status"] = "ok"
            ledger["turns_graded"] += 1
    except Exception as e:  # a broken judge must never break the session
        with chm.locked_ledger(payload) as ledger:
            ledger["judge_status"] = f"error: {str(e)[:120]}"
        chm.log(f"[{sid[:8]}] judge failed: {e}")
