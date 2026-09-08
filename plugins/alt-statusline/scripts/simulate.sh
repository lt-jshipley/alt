#!/bin/bash
# Fires fake hook payloads at the scripts without a live Claude Code session.
# No real model call: sections 0-10 disable the judge (CHM_NO_JUDGE=1) and
# section 11 puts a fake `claude` on PATH that sleeps and prints a canned
# verdict, so it tests only deterministic plumbing: the activation gate, the
# canary, counters, grading, warning cadence, reply clipping, git segment,
# token display, degraded payloads (schema drift), the setup.py install/remove
# round trip, the launcher's plugin-root resolution, and the concurrency rules
# (ledger lock, registry lock, serialized Stops, prompt attribution, judge
# isolation flags).
# Runs against throwaway state and HOME dirs; touches nothing real.
set -e
SCRIPTS="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(dirname "$SCRIPTS")"
export CHM_STATE_DIR="$(mktemp -d)"
export PYTHONPATH="$SCRIPTS"
export CHM_NO_JUDGE=1
FAKE_HOME="$(mktemp -d)"
trap 'rm -rf "$CHM_STATE_DIR" "$FAKE_HOME"' EXIT
STATE="$CHM_STATE_DIR"
SID="simtest-$$"
PY="$(command -v python3)"                  # absolute: some checks run hooks with PATH emptied
hook() { "$PY" "$SCRIPTS/$1" "${@:2}"; }    # hook <script> [args], payload on stdin
ledger() { python3 -c "import json,sys;print(json.dumps(json.load(open('$STATE/sessions/$1.json'))$2))"; }

echo "--- state: $STATE  session: $SID"

echo "--- 0a. GATE: no registry -> every hook is inert (no ledger, no stdout)"
for script_args in "on_counter.py tool_calls" "on_counter.py tool_failures" "on_prompt_submit.py" "on_stop.py" "on_session_start.py fresh" "on_session_start.py compact"; do
  OUT=$(hook $script_args <<EOF
{"session_id":"$SID","cwd":"/nowhere","prompt":"x","last_assistant_message":"y"}
EOF
)
  [ -z "$OUT" ] || { echo "FAIL: $script_args printed while inert: $OUT"; exit 1; }
done
[ ! -e "$STATE/sessions" ] || { echo "FAIL: inert hooks wrote state"; exit 1; }
echo "gate holds — ok"

echo "--- 0b. registry present -> active for the rest of the run (stale plugin root; section 0 refreshes it)"
mkdir -p "$STATE/sessions"
cat > "$STATE/install.json" <<EOF
{"plugin_root":"/stale/root","user":{"settings_file":"x","had_previous":false,"previous_statusline":null,"installed_at":"t"}}
EOF
python3 -c 'import chm_common as chm; assert chm.is_active()'

echo "--- 0. fresh session start (canary; must print nothing; stamps + refreshes the plugin root)"
OUT=$(env CLAUDE_PLUGIN_ROOT="$PLUGIN_ROOT" "$PY" "$SCRIPTS/on_session_start.py" fresh <<EOF
{"session_id":"$SID","hook_event_name":"SessionStart","source":"startup"}
EOF
)
[ -z "$OUT" ] || { echo "FAIL: fresh start printed: $OUT"; exit 1; }
[ "$(ledger $SID "['plugin_root']")" = "\"$PLUGIN_ROOT\"" ] || { echo "FAIL: plugin_root not stamped: $(ledger $SID "['plugin_root']")"; exit 1; }
python3 -c "import chm_common as chm; r = chm.load_registry(); assert r['plugin_root'] == '$PLUGIN_ROOT' and r['user'], r"
echo "plugin root stamped in the ledger, registry refreshed — ok"

echo "--- 0c. canary: no claude on PATH is fine in counters-only mode, an error otherwise, cleared once fixed"
RESUME="{\"session_id\":\"$SID\",\"hook_event_name\":\"SessionStart\",\"source\":\"resume\"}"
echo "$RESUME" | env PATH=/nonexistent CHM_NO_JUDGE=1 "$PY" "$SCRIPTS/on_session_start.py" fresh
[ "$(ledger $SID "['judge_status']")" = '"pending"' ] || { echo "FAIL: counters-only canary complained: $(ledger $SID "['judge_status']")"; exit 1; }
echo "$RESUME" | env -u CHM_NO_JUDGE PATH=/nonexistent "$PY" "$SCRIPTS/on_session_start.py" fresh
ledger $SID "['judge_status']" | grep -q "error: canary: claude not on PATH" || { echo "FAIL: missing claude not flagged: $(ledger $SID "['judge_status']")"; exit 1; }
FAKEBIN="$(mktemp -d)"; printf '#!/bin/sh\nexit 0\n' > "$FAKEBIN/claude"; chmod +x "$FAKEBIN/claude"
echo "$RESUME" | env -u CHM_NO_JUDGE PATH="$FAKEBIN" "$PY" "$SCRIPTS/on_session_start.py" fresh
rm -rf "$FAKEBIN"
[ "$(ledger $SID "['judge_status']")" = '"pending"' ] || { echo "FAIL: fixed canary did not clear: $(ledger $SID "['judge_status']")"; exit 1; }
echo "canary honors CHM_NO_JUDGE, flags a missing claude, clears when fixed — ok"

echo "--- 1. user submits a prompt"
hook on_prompt_submit.py <<EOF
{"session_id":"$SID","hook_event_name":"UserPromptSubmit","prompt":"Fix the billing proration bug in invoice.py"}
EOF

echo "--- 2. two tools succeed, one fails"
hook on_counter.py tool_calls <<EOF
{"session_id":"$SID","hook_event_name":"PostToolUse","tool_name":"Read"}
EOF
hook on_counter.py tool_calls <<EOF
{"session_id":"$SID","hook_event_name":"PostToolUse","tool_name":"Edit"}
EOF
hook on_counter.py tool_failures <<EOF
{"session_id":"$SID","hook_event_name":"PostToolUseFailure","tool_name":"Bash","error":"Exit code 1\nFAILED test_invoice.py::test_proration"}
EOF

echo "--- 2b. three more rapid failures -> burst elevates (yellow, never red alone); a success resets the streak"
for i in 1 2 3; do
  hook on_counter.py tool_failures <<EOF
{"session_id":"$SID","hook_event_name":"PostToolUseFailure","tool_name":"Bash","error":"Exit code 1"}
EOF
done
python3 - "$SID" <<'PYEOF'
import sys, chm_common as chm
led = chm.load_ledger(sys.argv[1])
assert led["fail_streak"] == 4, led["fail_streak"]
level, reasons, flags = chm.grade(led)
assert level == "minor" and "fails" in flags, (level, reasons)
PYEOF
hook on_counter.py tool_calls <<EOF
{"session_id":"$SID","hook_event_name":"PostToolUse","tool_name":"Read"}
EOF
python3 - "$SID" <<'PYEOF'
import sys, chm_common as chm
led = chm.load_ledger(sys.argv[1])
assert led["fail_streak"] == 0, led["fail_streak"]
print("streak/burst: elevated while live, reset on success — ok")
PYEOF

echo "--- 3. turn ends (judge disabled); the prompt was queued >1s ago so this Stop consumes it"
sleep 1.1
hook on_stop.py <<EOF
{"session_id":"$SID","hook_event_name":"Stop","stop_hook_active":false,"last_assistant_message":"I tried moving the rounding but tests still fail; I will investigate the date math next."}
EOF
python3 - "$SID" <<'PYEOF'
import sys, chm_common as chm
led = chm.load_ledger(sys.argv[1])
stat = led["turn_stats"][-1]
assert stat["msg_len"] > 0 and stat["duration_s"] >= 1 and stat["turn"] == 1, stat
assert led["judge_status"] == "disabled", led["judge_status"]
assert led["pending_prompts"] == [], led["pending_prompts"]
print("turn_stats recorded, prompt consumed — ok")
PYEOF

echo "--- 3a. long replies: clipped head+tail for the judge, real length in turn_stats"
python3 - <<'PYEOF'
import chm_common as chm
long = "HEAD-SENTINEL " + "x" * 20000 + " TAIL-SENTINEL"
out = chm.clip_middle(long)
assert len(out) <= chm.MSG_CLIP, len(out)
assert out.startswith("HEAD-SENTINEL") and out.endswith("TAIL-SENTINEL"), (out[:30], out[-30:])
assert "elided" in out, out[2900:3100]
assert chm.clip_middle("short") == "short"
PYEOF
LONG_REPLY="$(python3 -c "print('y' * 20000, end='')")"
hook on_stop.py <<EOF
{"session_id":"$SID","hook_event_name":"Stop","stop_hook_active":false,"last_assistant_message":"$LONG_REPLY"}
EOF
python3 - "$SID" <<'PYEOF'
import sys, chm_common as chm
led = chm.load_ledger(sys.argv[1])
assert led["turn_stats"][-1]["msg_len"] == 20000, led["turn_stats"][-1]
print("clip_middle + full msg_len — ok")
PYEOF

echo "--- 3b. topics are per-session: record_topics touches only the ledger"
python3 - "$SID" <<'PYEOF'
import os, sys, chm_common as chm
led = chm.load_ledger(sys.argv[1])
chm.record_topics(led, ["Billing Proration", "billing-proration", ""])
assert led["topics"] == ["billing-proration"] and led["topic_counts"]["billing-proration"] == 2, led
assert not any(n.startswith("tags") for n in os.listdir(chm.STATE_DIR)), os.listdir(chm.STATE_DIR)
print("per-session topics, no shared vocabulary file — ok")
PYEOF

echo "--- 3c. same-issue correction streak (Anthropic clear-and-restart rule) is red on its own; legacy ledgers grade"
python3 - <<'PYEOF'
import chm_common as chm
led = chm.load_ledger("grade-check-ephemeral")  # never saved
led["correction_log"] = [{"desc": "stop editing the generated file", "count": 3}]
led["corrections"] = 3
assert chm.grade(led)[0] == "restart", chm.grade(led)
old = chm.load_ledger("grade-check-ephemeral")  # pre-upgrade ledger shape
del old["correction_log"], old["fail_streak"], old["fail_times"], old["pending_prompts"], old["turn"]
old["pending_user_prompt"] = "legacy single slot"
chm.grade(old)  # must not KeyError on old ledgers
chm.save_ledger(old)
print("correction streak red + legacy-ledger grade — ok")
PYEOF
echo '{"session_id":"grade-check-ephemeral","last_assistant_message":"reply"}' | hook on_stop.py
python3 - <<'PYEOF'
import chm_common as chm
led = chm.load_ledger("grade-check-ephemeral")
assert led["judge_status"] == "disabled" and led["turn_stats"], led
print("legacy ledger through on_stop — ok")
PYEOF

echo "--- 4. compaction fires (stdout below is what Claude would receive)"
hook on_session_start.py compact <<EOF
{"session_id":"$SID","hook_event_name":"SessionStart","source":"compact"}
EOF

echo "--- 5. statusline render"
python3 "$SCRIPTS/statusline.py" <<EOF
{"session_id":"$SID","model":{"display_name":"Fable 5"},"context_window":{"used_percentage":42.7}}
EOF

echo "--- 5b. git segment: dirty-state split + default-branch warn + per-session cache"
GITDIR=$(mktemp -d)
git -C "$GITDIR" init -q -b main
git -C "$GITDIR" -c user.email=t@t -c user.name=t commit -q --allow-empty -m init
echo b > "$GITDIR/tracked.txt"
git -C "$GITDIR" add tracked.txt
git -C "$GITDIR" -c user.email=t@t -c user.name=t commit -q -m c2
echo c >> "$GITDIR/tracked.txt"                                   # unstaged
echo d > "$GITDIR/staged.txt"; git -C "$GITDIR" add staged.txt    # staged
echo e > "$GITDIR/untracked.txt"                                  # untracked
OUT=$(python3 "$SCRIPTS/statusline.py" <<EOF
{"session_id":"$SID","workspace":{"current_dir":"$GITDIR"}}
EOF
)
echo "$OUT" | head -1
for tok in "⚠ main" "+1" "!1" "?1"; do
  echo "$OUT" | grep -qF "$tok" || { echo "FAIL: git segment missing '$tok'"; exit 1; }
done
OUT2=$(python3 "$SCRIPTS/statusline.py" <<EOF
{"session_id":"$SID","workspace":{"current_dir":"$GITDIR"}}
EOF
)
[ -f "$STATE/sessions/$SID.git.json" ] || { echo "FAIL: per-session git cache not written"; exit 1; }
[ "$(echo "$OUT" | head -1)" = "$(echo "$OUT2" | head -1)" ] || { echo "FAIL: cached render differs"; exit 1; }
rm -rf "$GITDIR"
echo "git segment + cache — ok"

echo "--- 5c. token display: current_usage is an object per the docs; total_input_tokens is the live size"
OUT=$(python3 "$SCRIPTS/statusline.py" <<EOF
{"session_id":"$SID","context_window":{"used_percentage":12.4,"total_input_tokens":24000,"current_usage":{"input_tokens":20000,"cache_creation_input_tokens":1000,"cache_read_input_tokens":3000,"output_tokens":500}}}
EOF
)
echo "$OUT" | grep -qF "(24k)" || { echo "FAIL: token count not rendered: $OUT"; exit 1; }
OUT=$(python3 "$SCRIPTS/statusline.py" <<EOF
{"session_id":"$SID","context_window":{"used_percentage":12.4,"current_usage":{"input_tokens":20000,"cache_creation_input_tokens":1000,"cache_read_input_tokens":3000,"output_tokens":500}}}
EOF
)
echo "$OUT" | grep -qF "(24k)" || { echo "FAIL: token count not summed from current_usage: $OUT"; exit 1; }
python3 -c "import json; c=json.load(open('$STATE/sessions/$SID.ctx.json')); assert c['tokens']==24000, c"
echo "token display — ok"

echo "--- 6. warning injection check (force red: 3 STALE open loops; fresh ones never grade)"
python3 - "$SID" <<'PYEOF'
import sys, chm_common as chm
led = chm.load_ledger(sys.argv[1])
turn = led.get("turn", 0)
led["open_loops"] = [{"desc": f"loop {i}", "opened_turn": turn} for i in range(3)]
assert "loops" not in chm.grade(led)[2], chm.grade(led)  # fresh = in-flight work
led["turn"] = turn + 9  # let the same loops linger
level, _reasons, flags = chm.grade(led)
assert level == "restart" and "loops" in flags, chm.grade(led)
chm.save_ledger(led)
# two ordinary elevations (no red-capable signal) = moderate, not restart
mod = chm.load_ledger("moderate-check-ephemeral")
mod["turn"] = 10
mod["open_loops"] = [{"desc": "a", "opened_turn": 1}, {"desc": "b", "opened_turn": 1}]
mod["corrections"] = 2
assert chm.grade(mod)[0] == "moderate", chm.grade(mod)
PYEOF
OUT=$(hook on_prompt_submit.py <<EOF
{"session_id":"$SID","hook_event_name":"UserPromptSubmit","prompt":"now add a new feature"}
EOF
)
echo "$OUT"
echo "$OUT" | grep -q additionalContext || { echo "FAIL: red grade did not inject warning"; exit 1; }

echo "--- 6b. warning cadence: once per red episode, re-armed below red"
OUT=$(hook on_prompt_submit.py <<EOF
{"session_id":"$SID","hook_event_name":"UserPromptSubmit","prompt":"still red"}
EOF
)
[ -z "$OUT" ] || { echo "FAIL: warned twice in one red episode: $OUT"; exit 1; }
python3 - "$SID" <<'PYEOF'
import sys, chm_common as chm
led = chm.load_ledger(sys.argv[1])
assert led["warned_red"] is True, led.get("warned_red")
led["open_loops"] = []; led["counters"]["compactions"] = 0   # the episode ends
ctx = chm.load_ctx(sys.argv[1])
assert chm.grade(led, ctx)[0] != "restart", chm.grade(led, ctx)
chm.save_ledger(led)
PYEOF
OUT=$(hook on_prompt_submit.py <<EOF
{"session_id":"$SID","hook_event_name":"UserPromptSubmit","prompt":"calm again"}
EOF
)
[ -z "$OUT" ] || { echo "FAIL: injected below red: $OUT"; exit 1; }
[ "$(ledger $SID "['warned_red']")" = "false" ] || { echo "FAIL: warning did not re-arm below red"; exit 1; }
python3 - "$SID" <<'PYEOF'
import sys, chm_common as chm
led = chm.load_ledger(sys.argv[1])
led["open_loops"] = [{"desc": f"loop {i}", "opened_turn": 0} for i in range(3)]  # red again
chm.save_ledger(led)
PYEOF
OUT=$(hook on_prompt_submit.py <<EOF
{"session_id":"$SID","hook_event_name":"UserPromptSubmit","prompt":"red again"}
EOF
)
echo "$OUT" | grep -q additionalContext || { echo "FAIL: new red episode did not warn"; exit 1; }
echo "warning once per episode, re-armed below red — ok"

echo "--- 7. DEGRADED: empty payloads must not crash and must count to 'current'"
for script_args in "on_counter.py tool_failures" "on_prompt_submit.py" "on_stop.py" "on_session_start.py fresh"; do
  echo '{}' | hook $script_args
done
python3 - <<'PYEOF'
import chm_common as chm
led = chm.load_ledger("current")
assert led["counters"]["tool_failures"] == 1, led["counters"]
assert led["schema_drift"] == [], led["schema_drift"]  # empty payload is not drift
print("current.json: fail counted, no false drift — ok")
PYEOF

echo "--- 8. DEGRADED: non-empty payload MISSING expected fields -> drift flagged"
hook on_prompt_submit.py <<EOF
{"session_id":"$SID","hook_event_name":"UserPromptSubmit"}
EOF
sleep 1.1
hook on_stop.py <<EOF
{"session_id":"$SID","hook_event_name":"Stop"}
EOF
echo "statusline must show a drift warning:"
OUT=$(python3 "$SCRIPTS/statusline.py" <<EOF
{"session_id":"$SID","context_window":{"used_percentage":42.7}}
EOF
)
echo "$OUT"
echo "$OUT" | grep -q "drift:" || { echo "FAIL: drift warning missing"; exit 1; }

echo "--- 9. statusline never borrows another session's ledger: unknown session -> 'no data'"
OUT=$(echo '{"session_id":"never-seen"}' | python3 "$SCRIPTS/statusline.py")
echo "$OUT"
echo "$OUT" | grep -q "no data" || { echo "FAIL: expected 'Session: no data' (current.json exists but must not be shown)"; exit 1; }

echo "--- 10. setup.py install/remove round trip against a throwaway HOME"
export HOME="$FAKE_HOME"
mkdir -p "$HOME/.claude" "$FAKE_HOME/bin"
# fake judge: consumes stdin, sleeps FAKE_JUDGE_SLEEP (default 2), prints a canned verdict
cat > "$FAKE_HOME/bin/claude" <<'EOF'
#!/bin/sh
cat > /dev/null
printf '%s\n%s\n' "$PWD" "$*" > "$HOME/judge_args"   # what on_stop passed; checked in 11a
sleep "${FAKE_JUDGE_SLEEP:-2}"
echo '{"reasoning":"fake","topics":["billing"],"opened_loops":[],"closed_loops":[],"corrections":[{"desc":"fake correction","repeat_of":null}]}'
EOF
chmod +x "$FAKE_HOME/bin/claude"
export PATH="$FAKE_HOME/bin:$PATH"
SETUP="$SCRIPTS/setup.py"
rm -f "$STATE/install.json"  # start uninstalled

echo "--- 10a. existing statusLine with padding -> swapped, padding kept, backup exact, siblings untouched"
cat > "$HOME/.claude/settings.json" <<'EOF'
{"model": "x", "statusLine": {"type": "command", "command": "echo old", "padding": 1}, "note": "ünïcödé"}
EOF
cp "$HOME/.claude/settings.json" "$FAKE_HOME/seed.json"
python3 "$SETUP" install --plugin-root "$PLUGIN_ROOT"
python3 - "$HOME/.claude/settings.json" "$STATE/install.json" "$STATE/launcher.py" <<'PYEOF'
import json, sys
s = json.load(open(sys.argv[1])); reg = json.load(open(sys.argv[2])); launcher = sys.argv[3]
sl = s["statusLine"]
assert launcher in sl["command"] and sl["padding"] == 1, sl
assert s["model"] == "x" and s["note"] == "ünïcödé", s
assert "ünïcödé" in open(sys.argv[1], encoding="utf-8").read()  # not \u-escaped
assert reg["user"]["had_previous"] is True
assert reg["user"]["previous_statusline"] == {"type": "command", "command": "echo old", "padding": 1}
print("install: command swapped, padding kept, backup exact — ok")
PYEOF
echo "--- 10b. second install is a no-op; backup untouched"
python3 "$SETUP" install --plugin-root "$PLUGIN_ROOT" | grep -q "already installed" || { echo "FAIL: second install not idempotent"; exit 1; }
python3 - "$STATE/install.json" <<'PYEOF'
import json, sys
reg = json.load(open(sys.argv[1]))
assert reg["user"]["previous_statusline"]["command"] == "echo old", reg
print("idempotent — ok")
PYEOF
echo "--- 10c. status reports installed"
python3 "$SETUP" status | grep -q "installed: yes" || { echo "FAIL: status missing install"; exit 1; }
echo "--- 10d. remove restores the seed exactly (as JSON) and clears the registry"
python3 "$SETUP" remove
python3 - "$HOME/.claude/settings.json" "$FAKE_HOME/seed.json" "$STATE/install.json" <<'PYEOF'
import json, sys
assert json.load(open(sys.argv[1])) == json.load(open(sys.argv[2])), "restore differs"
reg = json.load(open(sys.argv[3]))
assert "user" not in reg, reg
print("remove: exact restore, registry cleared — ok")
PYEOF
python3 "$SETUP" status | grep -q "installed: no" || { echo "FAIL: status should say not installed"; exit 1; }
echo "--- 10e. no settings file at all -> install creates it; remove deletes the key"
rm -f "$HOME/.claude/settings.json"
python3 "$SETUP" install --plugin-root "$PLUGIN_ROOT" >/dev/null
python3 - "$STATE/install.json" <<'PYEOF'
import json, sys
reg = json.load(open(sys.argv[1])); assert reg["user"]["had_previous"] is False, reg
PYEOF
python3 "$SETUP" remove >/dev/null
python3 - "$HOME/.claude/settings.json" <<'PYEOF'
import json, sys
s = json.load(open(sys.argv[1])); assert "statusLine" not in s, s
print("no prior statusLine: key removed on remove — ok")
PYEOF
echo "--- 10f. invalid JSON in settings -> refuses, file untouched"
echo '{not json' > "$HOME/.claude/settings.json"
if python3 "$SETUP" install --plugin-root "$PLUGIN_ROOT" 2>/dev/null; then echo "FAIL: installed over invalid JSON"; exit 1; fi
[ "$(cat "$HOME/.claude/settings.json")" = '{not json' ] || { echo "FAIL: invalid settings file was modified"; exit 1; }
echo "invalid JSON refused — ok"
echo '{}' > "$HOME/.claude/settings.json"
python3 "$SETUP" install --plugin-root "$PLUGIN_ROOT" >/dev/null  # re-arm the gate for section 11

echo "--- 10g. launcher: session's own plugin root first, then registry, then cache; stdin re-supplied whole"
FAKEPLUG="$FAKE_HOME/fakeplugin"; mkdir -p "$FAKEPLUG/scripts"
cat > "$FAKEPLUG/scripts/statusline.py" <<'EOF'
import json, sys
raw = sys.stdin.read()
print("FAKE", json.loads(raw).get("session_id"), len(raw))
EOF
python3 - "$FAKEPLUG" <<'PYEOF'
import sys, chm_common as chm
led = chm.load_ledger("lsid"); led["plugin_root"] = sys.argv[1]; chm.save_ledger(led)
PYEOF
PAYLOAD='{"session_id":"lsid"}'
OUT=$(printf '%s' "$PAYLOAD" | python3 "$STATE/launcher.py")
[ "$OUT" = "FAKE lsid ${#PAYLOAD}" ] || { echo "FAIL: launcher ignored the session's plugin root: $OUT"; exit 1; }
BIG="$(python3 -c "import json; print(json.dumps({'session_id': 'lsid', 'filler': 'z' * 100000}), end='')")"
OUT=$(printf '%s' "$BIG" | python3 "$STATE/launcher.py")
[ "$OUT" = "FAKE lsid ${#BIG}" ] || { echo "FAIL: 100KB payload not passed through whole: ${OUT:0:80}"; exit 1; }
rm -rf "$FAKEPLUG"
OUT=$(printf '%s' "$PAYLOAD" | python3 "$STATE/launcher.py")
echo "$OUT" | grep -q "Session:" || { echo "FAIL: registry fallback did not render: $OUT"; exit 1; }
CACHED="$HOME/.claude/plugins/cache/m/alt-statusline/9.9.9/scripts"; mkdir -p "$CACHED"
printf 'print("CACHED")\n' > "$CACHED/statusline.py"
python3 -c "import chm_common as chm; chm.update_registry(lambda r: r.__setitem__('plugin_root', '/bogus/root'))"
OUT=$(printf '%s' '{}' | python3 "$STATE/launcher.py")
[ "$OUT" = "CACHED" ] || { echo "FAIL: cache fallback did not run: $OUT"; exit 1; }
rm -rf "$HOME/.claude/plugins"
RC=0; OUT=$(printf '%s' '{}' | python3 "$STATE/launcher.py") || RC=$?
[ $RC -eq 0 ] && echo "$OUT" | grep -q "plugin not found" || { echo "FAIL: nothing-found case should print the dim line and exit 0 (rc=$RC): $OUT"; exit 1; }
python3 -c "import chm_common as chm; chm.update_registry(lambda r: r.__setitem__('plugin_root', '$PLUGIN_ROOT'))"
echo "launcher: ledger root, registry root, cache, not-found — ok"

echo "--- 11. CONCURRENCY (fake judge on PATH, judge enabled for this section only)"
unset CHM_NO_JUDGE
CSID="conc-$$"
prompt() { hook on_prompt_submit.py <<EOF
{"session_id":"$CSID","hook_event_name":"UserPromptSubmit","prompt":"$1"}
EOF
}
stop() { hook on_stop.py <<EOF
{"session_id":"$CSID","hook_event_name":"Stop","stop_hook_active":false,"last_assistant_message":"$1"}
EOF
}
tool() { echo "{\"session_id\":\"$CSID\"}" | hook on_counter.py tool_calls; }

echo "--- 11a. RACE: async Stop mid-judge must not clobber the next turn's writes"
prompt "first"; sleep 1.1
stop "reply one" & STOP1=$!
sleep 0.4
prompt "second"; tool; tool
wait $STOP1
python3 - "$CSID" <<'PYEOF'
import sys, chm_common as chm
led = chm.load_ledger(sys.argv[1])
assert led["turn"] == 2, led["turn"]
assert led["counters"]["tool_calls"] == 2, led["counters"]
assert [p["prompt"] for p in led["pending_prompts"]] == ["second"], led["pending_prompts"]
assert led["topics"] == ["billing"] and led["corrections"] == 1 and led["turns_graded"] == 1, led
assert led["judge_status"] == "ok", led["judge_status"]
print("race: concurrent writes kept, next prompt left for its own Stop — ok")
PYEOF
python3 - "$STATE" "$HOME/judge_args" <<'PYEOF'
import os, sys
cwd, args = (open(sys.argv[2]).read().splitlines() + ["", ""])[:2]
assert os.path.realpath(cwd) == os.path.realpath(sys.argv[1]), (cwd, sys.argv[1])
for flag in ("--system-prompt-file", "--tools", "--no-session-persistence", "--strict-mcp-config"):
    assert flag in args, (flag, args)
print("judge isolated: run from the state dir with its own system prompt — ok")
PYEOF

echo "--- 11b. OVERLAPPING STOPS: the second waits for the first's judge, then grades from a fresh snapshot"
sleep 1.1                       # "second" is now old enough for Stop 2
stop "reply two" & STOP2=$!
sleep 0.3
prompt "third"; sleep 1.1
stop "reply three" & STOP3=$!
wait $STOP2 $STOP3
python3 - "$CSID" <<'PYEOF'
import sys, chm_common as chm
led = chm.load_ledger(sys.argv[1])
assert led["turns_graded"] == 3 and led["corrections"] == 3, (led["turns_graded"], led["corrections"])
assert led["topics"] == ["billing"] and led["topic_counts"]["billing"] == 3, (led["topics"], led["topic_counts"])
assert led["pending_prompts"] == [], led["pending_prompts"]
turns = [s["turn"] for s in led["turn_stats"]]
assert turns == [1, 2, 3], turns
print("overlapping Stops serialized, each attributed to its own turn — ok")
PYEOF

echo "--- 11c. PARALLEL COUNTERS: ten at once, ten counted"
for i in $(seq 10); do tool & done; wait
python3 - "$CSID" <<'PYEOF'
import sys, chm_common as chm
led = chm.load_ledger(sys.argv[1])
assert led["counters"]["tool_calls"] == 12, led["counters"]
print("parallel counters — ok")
PYEOF

echo "--- 11d. JUDGE-LOCK EXPIRY: a Stop that can't get the judge in time skips, never blocks the session"
prompt "fourth"; sleep 1.1
FAKE_JUDGE_SLEEP=5 stop "reply four" & STOP4=$!
sleep 0.4
prompt "fifth"; sleep 1.1
CHM_JUDGE_WAIT_S=0.5 stop "reply five"     # foreground: returns after ~0.5s
python3 - "$CSID" <<'PYEOF'
import sys, chm_common as chm
led = chm.load_ledger(sys.argv[1])
assert str(led["judge_status"]).startswith("skipped"), led["judge_status"]
assert led["pending_prompts"] == [], led["pending_prompts"]  # consumed even though not graded
PYEOF
wait $STOP4
python3 - "$CSID" <<'PYEOF'
import sys, chm_common as chm
led = chm.load_ledger(sys.argv[1])
assert led["judge_status"] == "ok" and led["turns_graded"] == 4, (led["judge_status"], led["turns_graded"])
print("judge-lock expiry: skipped cleanly, first Stop finished — ok")
PYEOF

echo "--- 11e. REGISTRY RACE: concurrent session starts can't resurrect a removed install record"
for i in $(seq 10); do
  echo "{\"session_id\":\"race-$i\"}" | env CLAUDE_PLUGIN_ROOT="$FAKE_HOME/root-$i" "$PY" "$SCRIPTS/on_session_start.py" fresh &
done
python3 "$SETUP" remove >/dev/null
wait
python3 - <<'PYEOF'
import chm_common as chm
reg = chm.load_registry()
assert "user" not in reg, reg
print("registry race: install record stays removed — ok")
PYEOF
python3 "$SETUP" install --plugin-root "$PLUGIN_ROOT" >/dev/null

echo "--- all checks passed"
