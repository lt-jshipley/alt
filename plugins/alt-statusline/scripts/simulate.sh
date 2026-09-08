#!/bin/bash
# Fires fake hook payloads at the scripts without a live Claude Code session.
# Judge is disabled (CHM_NO_JUDGE=1) so this tests only the deterministic
# plumbing: the activation gate, counters, grading, git segment, degraded
# payloads (schema-drift handling), and the setup.py install/remove round trip.
# Runs against throwaway state and HOME dirs; touches nothing real.
set -e
SCRIPTS="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_ROOT="$(dirname "$SCRIPTS")"
export CHM_STATE_DIR="$(mktemp -d)"
export PYTHONPATH="$SCRIPTS"
export CHM_NO_JUDGE=1
unset CLAUDE_PROJECT_DIR
FAKE_HOME="$(mktemp -d)"
trap 'rm -rf "$CHM_STATE_DIR" "$FAKE_HOME"' EXIT
STATE="$CHM_STATE_DIR"
SID="simtest-$$"
hook() { python3 "$SCRIPTS/$1" "${@:2}"; }  # hook <script> [args], payload on stdin

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

echo "--- 0b. GATE: folder scope covers the registered root and its subdirectories only"
mkdir -p "$STATE/sessions"
cat > "$STATE/install.json" <<EOF
{"plugin_root":"$PLUGIN_ROOT","folders":{"/registered/repo":{"settings_file":"x","had_previous":false,"previous_statusline":null,"installed_at":"t"}}}
EOF
python3 - <<'PYEOF'
import os, chm_common as chm
assert chm.is_active({"cwd": "/registered/repo"})
assert chm.is_active({"cwd": "/registered/repo/sub/dir"})
assert not chm.is_active({"cwd": "/registered/repo-other"})
assert not chm.is_active({"cwd": "/elsewhere"})
os.environ["CLAUDE_PROJECT_DIR"] = "/registered/repo"
assert chm.is_active({"cwd": "/elsewhere"})  # launch dir wins over a wandering cwd
del os.environ["CLAUDE_PROJECT_DIR"]
print("folder gate: root + subdirs, launch dir over cwd — ok")
PYEOF

echo "--- 0c. registry: user scope -> active everywhere for the rest of the run"
cat > "$STATE/install.json" <<EOF
{"plugin_root":"$PLUGIN_ROOT","user":{"settings_file":"x","had_previous":false,"previous_statusline":null,"installed_at":"t"}}
EOF

echo "--- 0. fresh session start (canary; must print nothing)"
hook on_session_start.py fresh <<EOF
{"session_id":"$SID","hook_event_name":"SessionStart","source":"startup"}
EOF

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

echo "--- 3. turn ends (judge disabled)"
hook on_stop.py <<EOF
{"session_id":"$SID","hook_event_name":"Stop","stop_hook_active":false,"last_assistant_message":"I tried moving the rounding but tests still fail; I will investigate the date math next."}
EOF
python3 - "$SID" <<'PYEOF'
import sys, chm_common as chm
led = chm.load_ledger(sys.argv[1])
stat = led["turn_stats"][-1]
assert stat["msg_len"] > 0 and "duration_s" in stat, stat
assert led["judge_status"] == "disabled", led["judge_status"]
print("turn_stats recorded — ok")
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

echo "--- 3c. same-issue correction streak (Anthropic clear-and-restart rule) is red on its own"
python3 - <<'PYEOF'
import chm_common as chm
led = chm.load_ledger("grade-check-ephemeral")  # never saved
led["correction_log"] = [{"desc": "stop editing the generated file", "count": 3}]
led["corrections"] = 3
assert chm.grade(led)[0] == "restart", chm.grade(led)
old = chm.load_ledger("grade-check-ephemeral")  # pre-upgrade ledger shape
del old["correction_log"], old["fail_streak"], old["fail_times"]
chm.grade(old)  # must not KeyError on old ledgers
print("correction streak red + legacy-ledger grade — ok")
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
printf '#!/bin/sh\nexit 0\n' > "$FAKE_HOME/bin/claude"; chmod +x "$FAKE_HOME/bin/claude"
export PATH="$FAKE_HOME/bin:$PATH"
SETUP="$SCRIPTS/setup.py"
rm -f "$STATE/install.json"  # start uninstalled

echo "--- 10a. existing statusLine with padding -> swapped, padding kept, backup exact, siblings untouched"
cat > "$HOME/.claude/settings.json" <<'EOF'
{"model": "x", "statusLine": {"type": "command", "command": "echo old", "padding": 1}, "note": "ünïcödé"}
EOF
cp "$HOME/.claude/settings.json" "$FAKE_HOME/seed.json"
python3 "$SETUP" install --scope user --plugin-root "$PLUGIN_ROOT"
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
python3 "$SETUP" install --scope user --plugin-root "$PLUGIN_ROOT" | grep -q "already installed" || { echo "FAIL: second install not idempotent"; exit 1; }
python3 - "$STATE/install.json" <<'PYEOF'
import json, sys
reg = json.load(open(sys.argv[1]))
assert reg["user"]["previous_statusline"]["command"] == "echo old", reg
print("idempotent — ok")
PYEOF
echo "--- 10c. status lists user scope"
python3 "$SETUP" status | grep -q "installed: user" || { echo "FAIL: status missing user scope"; exit 1; }
echo "--- 10d. remove restores the seed exactly (as JSON) and clears the registry"
python3 "$SETUP" remove --scope user
python3 - "$HOME/.claude/settings.json" "$FAKE_HOME/seed.json" "$STATE/install.json" <<'PYEOF'
import json, sys
assert json.load(open(sys.argv[1])) == json.load(open(sys.argv[2])), "restore differs"
reg = json.load(open(sys.argv[3]))
assert "user" not in reg, reg
print("remove: exact restore, registry cleared — ok")
PYEOF
echo "--- 10e. no settings file at all -> install creates it; remove deletes the key"
rm -f "$HOME/.claude/settings.json"
python3 "$SETUP" install --scope user --plugin-root "$PLUGIN_ROOT" >/dev/null
python3 - "$STATE/install.json" <<'PYEOF'
import json, sys
reg = json.load(open(sys.argv[1])); assert reg["user"]["had_previous"] is False, reg
PYEOF
python3 "$SETUP" remove --scope user >/dev/null
python3 - "$HOME/.claude/settings.json" <<'PYEOF'
import json, sys
s = json.load(open(sys.argv[1])); assert "statusLine" not in s, s
print("no prior statusLine: key removed on remove — ok")
PYEOF
echo "--- 10f. invalid JSON in settings -> refuses, file untouched"
echo '{not json' > "$HOME/.claude/settings.json"
if python3 "$SETUP" install --scope user --plugin-root "$PLUGIN_ROOT" 2>/dev/null; then echo "FAIL: installed over invalid JSON"; exit 1; fi
[ "$(cat "$HOME/.claude/settings.json")" = '{not json' ] || { echo "FAIL: invalid settings file was modified"; exit 1; }
echo "invalid JSON refused — ok"
echo "--- 10g. folder scope from a subdirectory lands at the repo root; gate keyed on the root"
REPO="$(cd "$(mktemp -d)" && pwd -P)"
git -C "$REPO" init -q -b main; mkdir -p "$REPO/src/deep"
python3 "$SETUP" install --scope folder --folder "$REPO/src/deep" --plugin-root "$PLUGIN_ROOT" | tee "$FAKE_HOME/folder-install.out"
[ -f "$REPO/.claude/settings.local.json" ] || { echo "FAIL: local settings not at repo root"; exit 1; }
if ! git -C "$REPO" check-ignore -q .claude/settings.local.json; then
  grep -q "warning: add" "$FAKE_HOME/folder-install.out" || { echo "FAIL: missing gitignore warning"; exit 1; }
fi
python3 - "$STATE/install.json" "$REPO" <<'PYEOF'
import json, os, sys, chm_common as chm
reg = json.load(open(sys.argv[1])); root = os.path.realpath(sys.argv[2])
assert root in reg["folders"], (root, reg)
assert chm.is_active({"cwd": os.path.join(root, "src")})
assert not chm.is_active({"cwd": "/elsewhere"})
print("folder scope: repo root, gate active in subdir only — ok")
PYEOF
python3 "$SETUP" remove --scope folder --folder "$REPO/src" >/dev/null
python3 - "$REPO/.claude/settings.local.json" "$STATE/install.json" <<'PYEOF'
import json, sys
assert "statusLine" not in json.load(open(sys.argv[1]))
assert "folders" not in json.load(open(sys.argv[2]))
print("folder remove — ok")
PYEOF
rm -rf "$REPO"

echo "--- all checks passed"
