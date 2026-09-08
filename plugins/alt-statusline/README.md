# alt-statusline

A "sharpness gauge" for Claude Code sessions, rendered live in the statusline.
Claude Code shows how *full* the context window is; this shows how *healthy*
the session is — topic drift, tool failures, open loops (approaches tried and
never resolved), repeated corrections.

Scope: this tool answers one question — **"should this session be restarted?"**
Preserving what a restart would lose (constraints, decisions, rejected
approaches) is the job of the surrounding ecosystem: handoff docs, memory
systems, workflows. Because that tooling makes restarts cheap, the gauge is
calibrated to fire early.

There is no daemon and no second session. The plugin is a set of short-lived
hook scripts that Claude Code spawns at events, writing to a per-session ledger
file. A one-shot model call ("the judge") tags topics and audits open loops at
each turn end; deterministic counters track everything else for free.

**Installing the plugin changes nothing by itself.** Every hook exits at once
until you run `/alt-statusline:setup`, which swaps the statusline in for every
session on this machine and switches the hooks on. `/alt-statusline:remove`
restores the previous statusline exactly and switches the hooks off.

## Install

Prerequisites: `python3` and `claude` on PATH (stdlib only, no packages);
macOS or Linux (the ledger lock uses `flock`).

```
/plugin marketplace add lt-jshipley/alt
/plugin install alt-statusline@agentic-leantechniques
/reload-plugins
/alt-statusline:setup
```

Setup writes `statusLine` into `~/.claude/settings.json`. It refuses, with one
line saying why, if `claude` or `python3` is missing, the state directory is
not writable, or the settings file is not valid JSON. It never leaves a
half-installed state: settings are written atomically, the registry second,
and settings roll back if the registry write fails.

Effects are immediate: Claude Code reloads settings on save, so the statusline
appears without a restart, and the hooks are live from the next event because
the plugin is already loaded.

`/alt-statusline:remove` restores the previous `statusLine` value (or deletes
the key if there was none), clears the registry, and keeps the session ledgers.

To keep the gauge but skip the per-turn model call in one project, set
`CHM_NO_JUDGE` to `1` in that project's settings `env` block (see Knobs).

## The statusline

```
Fable 5 · high | context-health-monitor ⚠ main +2 !3 ?1 ↑2        ← identity: model · effort | git
Session: Stable | 12% used (24k) | topics:2 · loops:1/4 · fails:1/31   ← the gauge
Topics: billing-proration:4 | invoice-tests:1                     ← judge's topic tags (session mention counts)
```

At red, the label is itself the call to action:

```
Session: Restart Recommended | 42% used (84k) | corrections:2 · compactions:1
```

Chips wear the grade color when they contributed to it; healthy chips stay
green. With no ledger yet for the session, the gauge row reads `Session: no
data`; it never borrows another session's grade. The token count in
parentheses is the live context size Claude Code reports (`total_input_tokens`).

Git symbols: `+staged !unstaged ?untracked =conflicts`, `⎇wt` linked worktree,
`⚠` working on the default branch, `REBASING`-style in-progress labels,
`DETACHED @sha`. Red = conflicts / in-progress op / default branch / detached;
yellow = dirty; green = clean. The git segment is cached per session for 5s;
`⚠` matches `main,master` (`CHM_DEFAULT_BRANCH` overrides, comma-separated).

## What gets graded

`Session: Stable | Drifting | Degrading | Restart Recommended` — no elevated
dimensions, one, two, or (three-plus / any Restart-capable signal). Scores are
ordinal, not cardinal: compare a session to your other sessions, not to a magic
threshold. The warning injection (a nudge added to your next turn) fires at
Restart only — Degrading informs, never nags.

| Signal | Source | Elevates | Restart on its own |
|---|---|---|---|
| Topics | judge, per-session vocabulary | 5+ distinct in one session | — |
| Open loops | judge; age-gated — a loop only counts once unresolved 3+ turns | 2+ stale | 3+ stale |
| Tool failures | counters (event identity only) | ≥5 failures at ≥10% of calls, or ≥15 total, or 4+ consecutive, or 3 inside 2 minutes — at most one elevation, whichever is most specific | — |
| User corrections | judge; repeats matched against prior corrections | 2+ in the session | same issue corrected 3+ times (Anthropic's clear-and-restart rule) |
| Compactions | SessionStart(compact) counter | — | any compaction |
| Context window | statusline sidecar | ≥25% full | ≥40% full |
| Monitor health | schema drift or judge error | degraded monitor elevates — the gauge fails loud, never as silent healthy zeros | — |

Grading notes, each a deliberate stance:

- **Loops are age-gated** on their `opened_turn`: a freshly opened loop is
  in-flight work, not clutter — and the ledger runs one async judge-cycle behind,
  so grading fresh loops made the gauge flap red on healthy sessions.
- **The failure dimension contributes one elevation total** — bursts are often
  environmental (network down, broken build) rather than context rot, so
  correlated failure conditions can never stack their way to Restart alone.
- **Compaction is amnesia, not fuzzy memory**: the summary replaces the
  transcript with no manifest of what was dropped, and the loss only surfaces
  behaviorally, after it bites. With restarts cheap, a compacted session gets
  restarted, not nursed.
- **Topics are per session.** The judge reuses the session's own topic list, so
  names stay consistent within a session and a genuinely new detour always
  mints a new tag. Nothing is shared between sessions; comparing sessions is a
  job for a later pass over the ledgers.

## How it works

```
hooks/hooks.json         plugin hook wiring; scripts referenced via ${CLAUDE_PLUGIN_ROOT}
scripts/
  chm_common.py          shared state library: ledger I/O, the two locks
                         (locked_ledger, judge_lock), the registry gate
                         is_active(), grade() — the single source of truth for
                         the gauge — and the payload ADAPTER: the only place hook
                         payload field names appear
  on_counter.py          pure event-identity counter (`on_counter.py <name>`):
                         which counter to bump comes from argv at registration,
                         not the payload; also tracks failure streaks/timestamps
  on_stop.py             Stop hook — consumes the turn's prompt, records per-turn
                         stats, runs the judge (serialized per session), applies
                         the verdict to a fresh ledger
  on_prompt_submit.py    UserPromptSubmit hook — stamps the turn, queues the
                         prompt for the judge, injects the Restart warning
  on_session_start.py    SessionStart hook, arg-driven by matcher: `compact`
                         counts the splice and re-injects the ledger across
                         compaction; `fresh` (startup|resume|clear|fork) runs the
                         canary and refreshes the registry's plugin root
  statusline.py          renders the ledger; computes nothing semantic
  launcher.py            template for the stable file the statusLine setting
                         points at (copied into the state dir by setup)
  setup.py               install / remove / status
  judge_prompt.md        instructions for the one-shot judge call
  simulate.sh            plumbing, gate, grading, concurrency, and setup
                         round-trip checks — no real model call
skills/setup, skills/remove
```

State lives outside the plugin, in `~/.claude/alt-statusline/`, which must be
on a local filesystem (`flock` is unreliable on network mounts):

```
install.json             registry: plugin root + the install record (settings
                         file and the backed-up statusLine)
launcher.py              what `statusLine.command` runs; execs the current
                         plugin's statusline.py, so plugin updates need no
                         settings change
sessions/<id>.json       per-session ledger (kept; resume reuses it)
sessions/<id>.json.lock  ledger lock (empty; never deleted)
sessions/<id>.judge.lock serializes Stops per session (empty; never deleted)
sessions/<id>.ctx.json   context-window sidecar written by the statusline
sessions/<id>.git.json   5s git-segment cache
chm.log                  debug log
```

Why a launcher: Claude Code installs plugins into a versioned cache directory
that changes on every update, so settings must never point into the plugin.
The launcher reads the plugin root from the registry, which the SessionStart
hook refreshes from `CLAUDE_PLUGIN_ROOT`; if that copy is gone it falls back to
the newest cached version, and if nothing is found it prints one dim line and
exits 0 rather than erroring on every render.

The ledger (stable keys, rankable across sessions):

```json
{
  "session_id": "…",
  "turn": 3,
  "counters": { "tool_calls": 0, "tool_failures": 0, "compactions": 0 },
  "topics": ["billing-proration"],
  "topic_counts": { "billing-proration": 4 },
  "open_loops": [{ "desc": "…", "opened_turn": 3 }],
  "closed_loops": 0,
  "corrections": 0,
  "correction_log": [{ "desc": "…", "count": 1 }],
  "fail_streak": 0,
  "fail_times": [1725800000.0],
  "pending_prompts": [{ "turn": 3, "prompt": "…", "ts": 1725800000.0 }],
  "turn_stats": [{ "turn": 3, "duration_s": 42, "msg_len": 1180 }],
  "turns_graded": 0,
  "last_warned_turn": 0,
  "judge_status": "ok",
  "schema_drift": []
}
```

`correction_log` entries grow a `count` when the judge flags a repeat.
`turn_stats` (per-turn duration and reply length) is recorded but never graded.
`judge_status` is `pending`, `ok`, `disabled`, `skipped: …`, or `error: …`;
only errors grade.

### Concurrency

Hooks are separate processes and overlap: parallel tool calls fire
`PostToolUse` concurrently, and the Stop hook is registered async, so it is
still running while the next turn's prompt and tool calls arrive. Two rules
keep the ledger honest:

- **Every ledger write holds an exclusive lock** around the whole
  read-modify-write, so no hook can overwrite another's increment. Holders keep
  it for milliseconds; the statusline only reads and needs no lock.
- **Stops are serialized per session.** The Stop hook consumes its prompt and
  records turn stats first, then takes the judge lock, snapshots the judge's
  input, runs the model call with no locks held, and applies the verdict by
  index to a freshly loaded ledger. Because only Stops write the judge-owned
  fields, the snapshot is exactly what the apply step sees. A Stop that cannot
  get the judge lock within `CHM_JUDGE_WAIT_S` (default 25s) marks the turn
  `skipped: busy` and exits rather than blocking.

Prompt attribution is by timestamp: a prompt queued within a second of a Stop
starting belongs to the next turn (input the user typed while Claude worked),
and prompts left behind by interrupted turns are dropped with a log line.

The judge is a one-shot call at each turn end. It sees only the turn delta plus
its own prior state, reasons before it answers (a `reasoning` field leads its
JSON schema), and is instructed to report nothing when unsure. It runs with all
hooks disabled, no tools, no session persistence, and an environment guard, so
it can never trigger this plugin's own hooks or leave transcripts behind. It
degrades gracefully: with no usable model call, the judge chip shows the error
and the deterministic counters keep working.

## Testing

`scripts/simulate.sh` fires fake hook payloads at the scripts against
throwaway state and HOME directories — the activation gate, counters, grading,
git segment, token display, degraded payloads, the setup install/remove round
trip, and the concurrency rules (a Stop mid-judge while the next turn writes,
two overlapping Stops, ten parallel counters, judge-lock expiry). It never
calls a real model: the judge is disabled, and the concurrency section uses a
fake `claude` on PATH that sleeps and prints a canned verdict.

The real judge path is checked by hand:

```
cd <some repo> && claude --plugin-dir /path/to/alt/plugins/alt-statusline
/alt-statusline:setup
```

Take two or three turns, including one typed while Claude is still working.
The gauge row should show no `judge:` chip and a `Topics:` row should appear.
Then `/alt-statusline:remove`.

## Schema independence

Hook payload JSON evolves between Claude Code releases, so the tool is built to
survive it: counters key off *which hook fired* (event + registration args) and
ignore the payload entirely; the few fields still read (`session_id`, `prompt`,
`last_assistant_message`, `error`) go through adapter accessors in
`chm_common.py`, so a rename is a one-file fix. When an expected field goes
missing from a non-empty payload, the ledger records `schema_drift` and the
statusline shows `⚠ drift:<field>` — never a silent healthy zero. Hook payloads
that can't provide a session id fall back to a shared `current.json` ledger so
counting never stops; the statusline never displays that ledger.

## Knobs & cost

The judge costs one Haiku call per turn end (roughly 8k prompt tokens with the
turn delta), in every session. Env knobs, settable per project in that
project's settings `env` block:

- `CHM_NO_JUDGE=1` — counters only, zero model calls (topics/loops/corrections
  stop updating)
- `CHM_JUDGE_MODEL` — model alias for the judge (default `haiku`)
- `CHM_JUDGE_EFFORT` — optional `--effort` (`low|medium|high|xhigh|max`)
- `CHM_JUDGE_WAIT_S` — how long a Stop waits for a running judge before
  skipping the turn (default `25`)
- `CHM_DEFAULT_BRANCH` — branches that trigger the git `⚠` (default `main,master`)

`CHM_STATE_DIR` relocates the state directory. It is a test override, not a
per-project knob: the launcher pins the state dir setup installed into.

## Limitations

- The ledger runs one async judge-cycle behind the conversation; the gauge is
  a trailing indicator by design.
- Stops are serialized per session, so a turn's grade can wait for the previous
  judge, and is skipped after `CHM_JUDGE_WAIT_S`.
- A turn that completes in under a second leaves its prompt for the next Stop,
  which drops it as an orphan; that reply is graded without its prompt.
- Sessions whose payloads can't provide an id share the `current.json` ledger.
- Grades are ordinal — meaningful against your own sessions, not as absolutes.
- Ledgers and lock files are kept indefinitely; there is no pruning yet.
- macOS and Linux only: the locks use `flock`, and `python3` must be on PATH
  under that name.
