"""Shared state I/O for alt-statusline (the context health monitor).

All hook scripts and the statusline import this. State lives in files under
STATE_DIR (default ~/.claude/alt-statusline, override with CHM_STATE_DIR) —
the monitor has no resident process, so this module IS the runtime between
events.

Concurrency: hooks are separate processes and several run at once (parallel
tool calls; the async Stop hook overlapping the next turn). Every ledger
mutation goes through locked_ledger(), an exclusive flock around the whole
read-modify-write; the Stop pipeline is additionally serialized per session by
judge_lock(); registry writes go through update_registry(), locked the same
way. Ledger files are written atomically (tmp + rename) so the
statusline, which only reads, needs no lock. flock is advisory and unreliable
on network filesystems; the state dir must be local.

Activation: hooks are inert until `setup.py install` writes install.json (the
registry) for this user. is_active() is the gate every hook passes through
before touching a ledger.
"""

import fcntl
import json
import os
import sys
import tempfile
import time
from contextlib import contextmanager
from datetime import datetime, timezone

STATE_DIR = os.environ.get("CHM_STATE_DIR") or os.path.expanduser("~/.claude/alt-statusline")
SESSIONS_DIR = os.path.join(STATE_DIR, "sessions")
LOG_PATH = os.path.join(STATE_DIR, "chm.log")
REGISTRY_PATH = os.path.join(STATE_DIR, "install.json")
LAUNCHER_PATH = os.path.join(STATE_DIR, "launcher.py")  # what statusLine points at

PENDING_PROMPTS_CAP = 5   # unconsumed prompts kept per session (interrupted turns)
LOCK_POLL_S = 0.25        # judge_lock retry interval


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def log(msg):
    """Append to the debug log; hooks must never crash the session, so
    scripts log failures here instead of raising."""
    try:
        os.makedirs(STATE_DIR, exist_ok=True)
        with open(LOG_PATH, "a") as f:
            f.write(f"{_now()} {msg}\n")
    except OSError:
        pass


def read_hook_payload():
    """Hook scripts receive their event payload as JSON on stdin."""
    try:
        return json.load(sys.stdin)
    except (json.JSONDecodeError, OSError) as e:
        log(f"bad hook payload: {e}")
        return {}


def atomic_write(path, data, strict=False):
    """tmp + rename. Logs and swallows OSError by default — hooks must never
    crash the session. strict=True re-raises after logging, for callers whose
    guarantees depend on seeing the failure (setup's settings rollback)."""
    tmp = None
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path))
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, indent=2)
        os.replace(tmp, path)
    except OSError as e:
        log(f"write failed {path}: {e}")
        if tmp:
            try:
                os.unlink(tmp)
            except OSError:
                pass
        if strict:
            raise


# ---------------------------------------------------------------------------
# Registry / activation gate.
#
# setup.py writes install.json when the user installs the statusline; remove
# deletes the entry. Hooks read it on every event and exit at once when it is
# absent, so an installed-but-not-set-up plugin grades nothing, calls no
# model, and injects nothing. Every write goes through update_registry(),
# which holds install.json.lock: setup and a starting session's plugin_root
# refresh must never interleave, or the install record gets dropped.
#
#   {"plugin_root": "...",                       last seen by SessionStart;
#                                                the launcher's fallback root
#    "user": {settings_file, had_previous, previous_statusline, installed_at}}
# ---------------------------------------------------------------------------

def load_registry():
    """Missing or unreadable registry means not installed."""
    try:
        with open(REGISTRY_PATH) as f:
            reg = json.load(f)
        return reg if isinstance(reg, dict) else {}
    except (OSError, json.JSONDecodeError):
        return {}


def update_registry(mutator):
    """Locked read-modify-write of install.json. mutator(reg) edits the dict
    in place; the file is rewritten only if it changed. Raises OSError on a
    failed write — setup must know; hooks catch and log."""
    fd = _lock_fd(REGISTRY_PATH + ".lock")
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        reg = load_registry()
        before = json.dumps(reg, sort_keys=True)
        mutator(reg)
        if json.dumps(reg, sort_keys=True) != before:
            atomic_write(REGISTRY_PATH, reg, strict=True)
        return reg
    finally:
        os.close(fd)


def is_active():
    """True once setup.py has installed the monitor for this user."""
    return bool(load_registry().get("user"))


def _empty_ledger(session_id):
    return {
        "session_id": session_id,
        "started_at": _now(),
        "updated_at": _now(),
        "turn": 0,                  # stamped by UserPromptSubmit
        "counters": {"tool_calls": 0, "tool_failures": 0, "compactions": 0},
        "topics": [],
        "topic_counts": {},     # per-session mentions: turns the judge tagged
        "open_loops": [],
        "closed_loops": 0,
        "corrections": 0,
        "correction_log": [],   # {desc, count} — count grows on judge-flagged repeats
        "fail_streak": 0,       # consecutive failures; any success resets it
        "fail_times": [],       # epoch seconds of recent failures (burst detection)
        "pending_prompts": [],  # {turn, prompt, ts} awaiting their Stop
        "turn_stats": [],       # {turn, duration_s, msg_len} — recorded, never graded
        "turns_graded": 0,
        "judge_status": "pending",  # pending | ok | disabled | skipped: ... | error: ...
        "schema_drift": [],         # payload fields expected but missing
        "warned_red": False,        # red warning fired this episode; cleared below red
        "plugin_root": None,        # CLAUDE_PLUGIN_ROOT at SessionStart; the launcher
                                    # renders this session with that plugin version
    }


def ledger_path(session_id):
    return os.path.join(SESSIONS_DIR, f"{session_id}.json")


def load_ledger(session_id):
    try:
        with open(ledger_path(session_id)) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return _empty_ledger(session_id)


def save_ledger(ledger):
    ledger["updated_at"] = _now()
    atomic_write(ledger_path(ledger["session_id"]), ledger)


def _lock_fd(path):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    return os.open(path, os.O_CREAT | os.O_RDWR, 0o644)


@contextmanager
def locked_ledger(payload):
    """Exclusive read-modify-write of the session ledger.

    Resolves the session id from the payload, falling back to the shared
    'current' ledger (and noting drift) when a non-empty payload can't provide
    one. Holds flock(LOCK_EX) on <ledger>.lock for the block, saves on clean
    exit or SystemExit, and does NOT save when the body raised anything else —
    a crash must not persist a half-mutated ledger. Holders keep the lock for
    milliseconds; nothing may hold it across the judge call. The lock is a
    separate file because _atomic_write swaps the ledger's inode; closing the
    descriptor (or the process dying) releases it."""
    payload = payload or {}
    sid = _first(payload, SESSION_ID_FIELDS) or "current"
    fd = _lock_fd(ledger_path(sid) + ".lock")
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        ledger = load_ledger(sid)
        if payload and sid == "current":
            note_drift(ledger, "session_id")
        try:
            yield ledger
        except SystemExit:
            save_ledger(ledger)
            raise
        except Exception as e:
            log(f"[{sid[:8]}] hook failed inside locked_ledger, not saved: {e!r}")
            raise
        else:
            save_ledger(ledger)
    finally:
        os.close(fd)


@contextmanager
def judge_lock(session_id, wait_s):
    """Serializes the Stop pipeline per session so two overlapping Stops can't
    grade from the same stale snapshot. Polls LOCK_NB up to wait_s and yields
    True if acquired, False on expiry. Lock order is judge, then ledger: never
    wait on this while holding locked_ledger."""
    fd = _lock_fd(os.path.join(SESSIONS_DIR, f"{session_id}.judge.lock"))
    acquired = False
    try:
        deadline = time.monotonic() + wait_s
        while True:
            try:
                fcntl.flock(fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
                acquired = True
                break
            except OSError:
                if time.monotonic() >= deadline:
                    break
                time.sleep(LOCK_POLL_S)
        yield acquired
    finally:
        os.close(fd)


# ---------------------------------------------------------------------------
# Grading — single source of truth for the statusline grade and the
# prompt-submit warning. Four tiers of drift:
#   stable    no elevated dimensions
#   minor     1 elevated dimension
#   moderate  2 elevated dimensions
#   restart   any red-capable signal — a compaction, a 40%+-full window,
#             the same issue corrected 3+ times (Anthropic's own
#             clear-and-restart rule), 3+ STALE open loops — or 3+
#             ordinary elevations
# ---------------------------------------------------------------------------

LOOP_STALE_TURNS = 3       # loops only grade once unresolved this many turns:
                           # a loop opened this turn is in-flight work, and the
                           # ledger runs one async judge-cycle behind — grading
                           # fresh loops made the gauge flap red on healthy work
GRADE_RED_OPEN_LOOPS = 3   # red on its own: stale unresolved accumulation
ELEV_OPEN_LOOPS = 2        # everything below only "elevates" (yellow)
ELEV_TOPICS = 5
ELEV_FAILS_MIN = 5         # failures elevate at >=5 AND >=10% of calls...
ELEV_FAILS_RATE = 0.10
ELEV_FAILS_ABS = 15        # ...or at >=15 regardless of rate
ELEV_FAIL_STREAK = 4       # ...or this many consecutive failures...
ELEV_FAIL_BURST_N = 3      # ...or a burst: this many consecutive failures
ELEV_FAIL_BURST_SECS = 120 #    inside this window. Bursts are often
                           #    environmental (network, broken build), so the
                           #    failure dimension only ever elevates — one
                           #    reason total, never red on its own
ELEV_CORRECTIONS = 2       # the "corrected twice -> /clear" heuristic
RED_CORRECTION_REPEAT = 3  # same issue corrected 3+ times: red-capable
ELEV_CTX_PCT = 25          # fractions of the model's window, straight from
RED_CTX_PCT = 40           # Claude Code's used_percentage (250k / 400k on a
                           # 1M window). 25%+ is one elevation; 40%+ is
                           # red-capable on its own. Window-relative on
                           # purpose: standing overhead (system prompt,
                           # CLAUDE.md, skills) alone can hit ~13% before work
                           # begins, so absolute-token rules mislead.


def ctx_path(session_id):
    """Sidecar for context-window readings — written by the statusline (the
    only surface that receives them), kept out of the ledger to avoid
    write races with the hooks."""
    return os.path.join(SESSIONS_DIR, f"{session_id}.ctx.json")


def load_ctx(session_id):
    try:
        with open(ctx_path(session_id)) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return {}


def save_ctx(session_id, pct, tokens):
    atomic_write(ctx_path(session_id), {"pct": pct, "tokens": tokens})


def stale_open_loops(ledger):
    """Open loops old enough to grade. The statusline shows the whole open
    count as "loose ends" and takes its color from the verdict, so display
    and grade stay consistent without repeating the age rule. Entries missing
    opened_turn count as stale (fail toward caution, never silence)."""
    turn = ledger.get("turn", 0)
    return [l for l in ledger["open_loops"]
            if turn - l.get("opened_turn", 0) >= LOOP_STALE_TURNS]


def grade(ledger, ctx=None):
    """Return ('stable'|'minor'|'moderate'|'restart', [reasons], {flag keys}).

    Flag keys name the dimensions that elevated — 'loops', 'topics', 'fails',
    'corrections', 'compactions', 'infra', 'context' — so the statusline can
    paint the offending chips in the band color."""
    c = ledger["counters"]
    loops = len(stale_open_loops(ledger))
    topics = len(ledger["topics"])
    fails = c["tool_failures"]
    total = c["tool_calls"] + fails

    reasons, flags = [], set()
    red_capable = False  # any one of these signals alone means restart

    def flag(key, reason):
        flags.add(key)
        reasons.append(reason)

    if loops >= ELEV_OPEN_LOOPS:
        flag("loops", f"{loops} open loops unresolved {LOOP_STALE_TURNS}+ turns")
        if loops >= GRADE_RED_OPEN_LOOPS:
            red_capable = True
    if topics >= ELEV_TOPICS:
        flag("topics", f"{topics} distinct topics in one session")
    # Failures: clustering (burst > streak) beats the flat rate as a signal,
    # but the dimension contributes at most ONE reason so correlated failure
    # conditions can never stack their way to red alone.
    streak = ledger.get("fail_streak", 0)
    times = ledger.get("fail_times", [])
    if (streak >= ELEV_FAIL_BURST_N and len(times) >= ELEV_FAIL_BURST_N
            and times[-1] - times[-ELEV_FAIL_BURST_N] <= ELEV_FAIL_BURST_SECS):
        flag("fails", f"{streak} consecutive failures within "
                      f"{ELEV_FAIL_BURST_SECS // 60} min")
    elif streak >= ELEV_FAIL_STREAK:
        flag("fails", f"{streak} consecutive tool failures")
    elif ((fails >= ELEV_FAILS_MIN and total and fails / total >= ELEV_FAILS_RATE)
            or fails >= ELEV_FAILS_ABS):
        flag("fails", f"{fails} tool failures ({round(100 * fails / total)}% of calls)")
    repeat = max((e.get("count", 1) for e in ledger.get("correction_log", [])),
                 default=0)
    if repeat >= RED_CORRECTION_REPEAT:
        flag("corrections", f"same issue corrected {repeat}x")
        red_capable = True
    elif ledger["corrections"] >= ELEV_CORRECTIONS:
        flag("corrections", f"{ledger['corrections']} user corrections")
    if c["compactions"] >= 1:
        # compaction is lossy with no manifest of what was dropped; with
        # restart workflows cheap, a compacted session should restart
        flag("compactions", f"{c['compactions']} compaction(s)")
        red_capable = True
    if (ledger.get("schema_drift")
            or str(ledger.get("judge_status", "")).startswith("error")):
        flag("infra", "monitor degraded (schema drift or judge error)")
    if ctx and ctx.get("pct") is not None:
        pct = ctx["pct"]
        if pct >= RED_CTX_PCT:
            flag("context", f"context window {round(pct)}% full")
            red_capable = True
        elif pct >= ELEV_CTX_PCT:
            flag("context", f"context window {round(pct)}% full")

    if red_capable or len(reasons) >= 3:
        return "restart", reasons, flags
    if len(reasons) == 2:
        return "moderate", reasons, flags
    if reasons:
        return "minor", reasons, flags
    return "stable", reasons, flags


# ---------------------------------------------------------------------------
# Payload adapter — the ONLY place hook payload field names appear.
#
# Design: the event firing is the fact; the payload is enrichment. Counters
# key off registration (event + argv), so an empty or reshaped payload can
# never zero the gauge. When a field this tool still depends on goes missing
# from a non-empty payload, that's schema drift: recorded on the ledger and
# rendered as a warning in the statusline — never a silent zero.
# Candidate lists are ordered current-name-first; a rename in a future
# Claude Code release is fixed by adding the new name here.
# ---------------------------------------------------------------------------

SESSION_ID_FIELDS = ["session_id"]
PROMPT_FIELDS = ["prompt"]
ASSISTANT_MSG_FIELDS = ["last_assistant_message"]
ERROR_FIELDS = ["error"]


def _first(payload, candidates):
    for name in candidates:
        val = payload.get(name)
        if val is not None:
            return val
    return None


def note_drift(ledger, field):
    drifts = ledger.setdefault("schema_drift", [])
    if field not in drifts:
        drifts.append(field)
        log(f"[{ledger['session_id'][:8]}] schema drift: expected payload "
            f"field '{field}' is missing")


def get_user_prompt(payload, ledger=None):
    val = _first(payload, PROMPT_FIELDS)
    if val is None and payload and ledger is not None:
        note_drift(ledger, "prompt")
    return val or ""


def get_assistant_message(payload):
    return _first(payload, ASSISTANT_MSG_FIELDS) or ""


def get_error(payload):
    """Optional log flavor only — absence is never drift."""
    return _first(payload, ERROR_FIELDS) or ""


def record_topics(ledger, topic_names):
    """Merge judge-returned topics into the session ledger. Topics are
    per-session: the judge reuses the ledger's own list, so names stay
    consistent within a session and never leak between sessions."""
    for name in topic_names:
        name = str(name).strip().lower().replace(" ", "-")[:40]
        if not name:
            continue
        if name not in ledger["topics"]:
            ledger["topics"].append(name)
        counts = ledger.setdefault("topic_counts", {})  # per-session mentions
        counts[name] = counts.get(name, 0) + 1


# ---------------------------------------------------------------------------
# Small shared helpers.
# ---------------------------------------------------------------------------

MSG_CLIP = 6000           # chars of the assistant reply the judge sees


def clip_middle(text, budget=MSG_CLIP):
    """Head + tail within budget, an elision marker between. The tail carries
    a reply's conclusions — what loop closures and corrections hinge on — so
    head-only truncation made the judge under-close loops."""
    if len(text) <= budget:
        return text
    marker = f"\n[... ~{len(text) - budget} chars elided ...]\n"
    keep = max(budget - len(marker), 0)
    head = keep // 2
    return text[:head] + marker + text[len(text) - (keep - head):]


def env_float(name, default):
    """Numeric env knob; a malformed value logs and falls back rather than
    crashing the hook at import."""
    raw = os.environ.get(name)
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        log(f"bad {name}={raw!r}; using {default}")
        return default
