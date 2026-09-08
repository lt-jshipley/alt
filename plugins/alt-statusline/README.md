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
until you run `/alt-statusline:setup`, which asks whether the gauge should run
for you everywhere or only in the current folder, swaps the statusline in, and
switches the hooks on. `/alt-statusline:remove` restores the previous
statusline exactly and switches the hooks off.

## Install

Prerequisites: `python3` and `claude` on PATH (stdlib only, no packages).

```
/plugin marketplace add lt-jshipley/alt
/plugin install alt-statusline@agentic-leantechniques
/reload-plugins
/alt-statusline:setup          (or: /alt-statusline:setup user | folder)
```

Scopes:

- **user** — every session on this machine. Writes `statusLine` into
  `~/.claude/settings.json`.
- **folder** — only sessions launched in this repository. Writes
  `.claude/settings.local.json` at the repository root (Claude Code reads the
  local file from there even when launched in a subdirectory). The file stays
  personal; setup warns if it is not gitignored.

Setup refuses, with one line saying why, if `claude` or `python3` is missing,
the state directory is not writable, or the target settings file is not valid
JSON. It never leaves a half-installed state: settings are written atomically,
the registry second, and settings roll back if the registry write fails.

Effects are immediate: Claude Code reloads settings on save, so the statusline
appears without a restart, and the hooks are live from the next event because
the plugin is already loaded. In a folder Claude Code has not trusted yet, the
statusline stays blank until the trust dialog is accepted.

`/alt-statusline:remove` restores the previous `statusLine` value (or deletes
the key if there was none), drops the scope from the registry, and keeps the
session ledgers.

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
data`; it never borrows another session's grade.

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
  chm_common.py          shared state library (ledger I/O), the registry gate
                         is_active(), grade() — the single source of truth for
                         the gauge — and the payload ADAPTER: the only place hook
                         payload field names appear
  on_counter.py          pure event-identity counter (`on_counter.py <name>`):
                         which counter to bump comes from argv at registration,
                         not the payload; also tracks failure streaks/timestamps
  on_stop.py             Stop hook — extracts the turn delta, records per-turn
                         stats, runs the judge, updates topics/loops/corrections
  on_prompt_submit.py    UserPromptSubmit hook — stamps the turn, captures the
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
  simulate.sh            plumbing, gate, grading, and setup round-trip checks
skills/setup, skills/remove
```

State lives outside the plugin, in `~/.claude/alt-statusline/` (override with
`CHM_STATE_DIR`):

```
install.json             registry: plugin root + the scopes setup installed, each
                         with its settings file and the backed-up statusLine
launcher.py              what `statusLine.command` runs; execs the current
                         plugin's statusline.py, so plugin updates need no
                         settings change
sessions/<id>.json       per-session ledger (kept; resume reuses it)
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
  "counters": { "tool_calls": 0, "tool_failures": 0, "compactions": 0 },
  "topics": ["billing-proration"],
  "topic_counts": { "billing-proration": 4 },
  "open_loops": [{ "desc": "…", "opened_turn": 3 }],
  "closed_loops": 0,
  "corrections": 0,
  "correction_log": [{ "desc": "…", "count": 1 }],
  "fail_streak": 0,
  "turn_stats": [{ "turn": 3, "duration_s": 42, "msg_len": 1180 }],
  "turns_graded": 0
}
```

`correction_log` entries grow a `count` when the judge flags a repeat.
`turn_stats` (per-turn duration and reply length) is recorded but never graded.

The judge is a one-shot call at each turn end. It sees only the turn delta plus
its own prior state, reasons before it answers (a `reasoning` field leads its
JSON schema), and is instructed to report nothing when unsure. It runs with all
hooks disabled and an environment guard, so it can never trigger this plugin's
own hooks. It degrades gracefully: with no usable model call, the judge chip
shows the error and the deterministic counters keep working.

## Testing

`scripts/simulate.sh` fires fake hook payloads at the scripts against
throwaway state and HOME directories — the activation gate, counters, grading,
git segment, degraded payloads, and the setup install/remove round trip
(existing statusline with padding, idempotent re-install, exact restore, no
prior statusline, invalid JSON refused, folder scope from a subdirectory).

For a live check without installing from the marketplace:

```
cd <some repo> && claude --plugin-dir /path/to/alt/plugins/alt-statusline
/alt-statusline:setup folder
```

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

The judge costs one Haiku call per turn end (a few hundred input tokens plus the
turn delta), in every session where the gauge is active. Env knobs, settable
per project in that project's settings `env` block:

- `CHM_NO_JUDGE=1` — counters only, zero model calls (topics/loops/corrections
  stop updating)
- `CHM_JUDGE_MODEL` — model alias for the judge (default `haiku`)
- `CHM_JUDGE_EFFORT` — optional `--effort` (`low|medium|high|xhigh|max`)
- `CHM_DEFAULT_BRANCH` — branches that trigger the git `⚠` (default `main,master`)
- `CHM_STATE_DIR` — state directory (default `~/.claude/alt-statusline`)

## Limitations

- The ledger runs one async judge-cycle behind the conversation; the gauge is
  a trailing indicator by design.
- Parallel tool calls can interleave the counter hooks; streak ordering is
  best-effort.
- Sessions whose payloads can't provide an id share the `current.json` ledger.
- Grades are ordinal — meaningful against your own sessions, not as absolutes.
- Ledgers are kept indefinitely; there is no pruning yet.
- `python3` must be on PATH under that name; there is no interpreter shim for
  Windows hosts yet.
