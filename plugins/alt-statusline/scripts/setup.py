#!/usr/bin/env python3
"""alt-statusline setup: install / remove / status.

  setup.py install [--plugin-root PATH]
  setup.py remove
  setup.py status

Run by the /alt-statusline:setup and :remove skills; safe to run by hand.
Exit 0 on success or nothing-to-do, 1 with a one-line reason on any failure.

Installs at user scope: the statusLine goes into ~/.claude/settings.json and
the hooks run in every session on this machine. Nothing half-done: preflight
first (claude and python3 on PATH, state dir writable, settings file valid
JSON, launcher smoke-tested), then the settings file is written atomically,
then the registry; if the registry write fails the settings file is rolled
back. `remove` restores the exact previous statusLine value, or deletes the
key when there was none.
"""

import argparse
import json
import os
import shlex
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import chm_common as chm  # noqa: E402

LAUNCHER_SRC = os.path.join(HERE, "launcher.py")
OLD_WIRING_MARKER = "context-health-monitor/scripts"  # the pre-plugin POC


def fail(msg):
    print(f"alt-statusline: {msg}", file=sys.stderr)
    sys.exit(1)


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def real(path):
    return os.path.realpath(os.path.expanduser(str(path)))


def settings_path():
    return os.path.expanduser("~/.claude/settings.json")


# ---------------------------------------------------------------------------
# JSON file I/O: atomic, mode-preserving, change-detecting
# ---------------------------------------------------------------------------

def read_json_object(path):
    """(data, mtime). Missing file -> ({}, None). Anything unparseable fails
    loudly instead of being overwritten."""
    if not os.path.exists(path):
        return {}, None
    try:
        with open(path, encoding="utf-8") as f:
            data = json.load(f)
    except json.JSONDecodeError as e:
        fail(f"{path} is not valid JSON ({e.msg} at line {e.lineno}); "
             "fix it first, nothing was changed")
    except OSError as e:
        fail(f"cannot read {path}: {e}")
    if not isinstance(data, dict):
        fail(f"{path} is not a JSON object; nothing was changed")
    return data, os.stat(path).st_mtime


def atomic_json(path, data, expected_mtime=None, default_mode=0o644):
    """Write JSON atomically in place. Raises OSError; callers decide.
    Aborts (RuntimeError) if the file changed since it was read — Claude Code
    writes settings files itself on permission approvals."""
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = default_mode
    if os.path.exists(path):
        st = os.stat(path)
        if expected_mtime is not None and st.st_mtime != expected_mtime:
            raise RuntimeError(f"{path} changed while setup was running")
        mode = st.st_mode & 0o777
    fd, tmp = tempfile.mkstemp(dir=os.path.dirname(path), prefix=".alt-statusline-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
            f.write("\n")
        os.chmod(tmp, mode)
        os.replace(tmp, path)
    except OSError:
        try:
            os.unlink(tmp)
        except OSError:
            pass
        raise


def write_settings(path, data, expected_mtime):
    try:
        atomic_json(path, data, expected_mtime)
    except RuntimeError as e:
        fail(f"{e}; nothing was changed, run again")
    except OSError as e:
        fail(f"cannot write {path}: {e}; nothing was changed")


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def resolve_plugin_root(arg):
    root = real(arg) if arg else os.path.dirname(HERE)
    if not os.path.isfile(os.path.join(root, "scripts", "statusline.py")):
        fail(f"{root} does not look like the alt-statusline plugin "
             "(scripts/statusline.py missing)")
    return root


def is_ours(statusline):
    return (isinstance(statusline, dict)
            and chm.LAUNCHER_PATH in str(statusline.get("command", "")))


# ---------------------------------------------------------------------------
# Preflight and warnings
# ---------------------------------------------------------------------------

def preflight(path, plugin_root):
    if not shutil.which("claude"):
        fail("`claude` is not on PATH; the judge needs it. Nothing was changed")
    if not shutil.which("python3"):
        fail("`python3` is not on PATH; the statusLine command needs it. "
             "Nothing was changed")
    try:
        os.makedirs(chm.SESSIONS_DIR, exist_ok=True)
    except OSError as e:
        fail(f"cannot create state dir {chm.STATE_DIR}: {e}")
    if not os.access(chm.STATE_DIR, os.W_OK):
        fail(f"state dir {chm.STATE_DIR} is not writable")
    data, mtime = read_json_object(path)

    # The launcher is refreshed on every install so fixes ship with updates,
    # and the registry learns the plugin root before the smoke test so the
    # launcher execs the real statusline rather than its not-found fallback.
    try:
        shutil.copyfile(LAUNCHER_SRC, chm.LAUNCHER_PATH)
    except OSError as e:
        fail(f"cannot write launcher {chm.LAUNCHER_PATH}: {e}")
    reg = chm.load_registry()
    if reg.get("plugin_root") != plugin_root:
        reg["plugin_root"] = plugin_root
        try:
            atomic_json(chm.REGISTRY_PATH, reg)
        except OSError as e:
            fail(f"cannot write registry {chm.REGISTRY_PATH}: {e}")
    try:
        r = subprocess.run([sys.executable, chm.LAUNCHER_PATH], input="{}",
                           capture_output=True, text=True, timeout=20,
                           env=dict(os.environ, CHM_STATE_DIR=chm.STATE_DIR))
    except (OSError, subprocess.TimeoutExpired) as e:
        fail(f"launcher smoke test could not run: {e}")
    if r.returncode != 0 or "plugin not found" in r.stdout:
        fail("launcher smoke test failed: "
             f"{(r.stderr or r.stdout).strip()[:200] or 'no output'}")
    return data, mtime, reg


def warnings():
    out = []
    shared = os.path.join(os.getcwd(), ".claude", "settings.json")
    try:
        with open(shared, encoding="utf-8") as f:
            if OLD_WIRING_MARKER in f.read():
                out.append(f"warning: {shared} still wires the pre-plugin monitor; "
                           "sessions started there will count every tool call "
                           "twice until those hooks are removed")
    except OSError:
        pass
    return out


# ---------------------------------------------------------------------------
# Commands
# ---------------------------------------------------------------------------

def cmd_install(args):
    path = settings_path()
    plugin_root = resolve_plugin_root(args.plugin_root)
    data, mtime, reg = preflight(path, plugin_root)
    current = data.get("statusLine")
    entry = reg.get("user")

    if entry and is_ours(current):
        print(f"already installed ({path}); nothing changed")
        return
    if entry and not is_ours(current):
        # registry says installed but the setting was changed by hand since:
        # re-take the display without disturbing the original backup
        print(f"re-installing the statusLine in {path} "
              "(registry entry kept, original backup untouched)")
    elif is_ours(current):
        # setting is ours but the registry lost the entry: hooks would be
        # inert while the display shows. Register with an honest empty backup.
        entry = {"settings_file": path, "had_previous": False,
                 "previous_statusline": None, "installed_at": now(),
                 "note": "registered after the fact; no backup was available"}
        print(f"statusLine in {path} was already ours; registering "
              "so the hooks run (no previous value to back up)")
    else:
        entry = {"settings_file": path,
                 "had_previous": "statusLine" in data,
                 "previous_statusline": current,
                 "installed_at": now()}

    for w in warnings():
        print(w)

    ours = {"type": "command", "command": f"python3 {shlex.quote(chm.LAUNCHER_PATH)}"}
    if isinstance(current, dict) and "padding" in current:
        ours["padding"] = current["padding"]
    new_data = dict(data)
    new_data["statusLine"] = ours
    write_settings(path, new_data, mtime)

    reg["user"] = entry
    try:
        atomic_json(chm.REGISTRY_PATH, reg)
    except OSError as e:
        write_settings(path, data, None)  # roll back
        fail(f"could not write registry {chm.REGISTRY_PATH}: {e}; "
             f"{path} was restored, nothing is installed")

    print(f"installed: statusLine in {path} -> {ours['command']}")
    print(f"active for every session on this machine; state in {chm.STATE_DIR}")
    if entry["had_previous"]:
        print(f"previous statusLine saved in {chm.REGISTRY_PATH}; "
              "/alt-statusline:remove restores it")
    else:
        print("there was no statusLine before; /alt-statusline:remove deletes the key")


def cmd_remove(_args):
    reg = chm.load_registry()
    entry = reg.get("user")
    if not entry:
        print("not installed; nothing changed")
        return
    path = entry.get("settings_file") or settings_path()
    data, mtime = read_json_object(path)
    current = data.get("statusLine")
    if not is_ours(current):
        print(f"{path} no longer carries the alt-statusline command; left as is")
    else:
        new_data = dict(data)
        if entry.get("had_previous"):
            new_data["statusLine"] = entry.get("previous_statusline")
            what = "restored the previous statusLine"
        else:
            new_data.pop("statusLine", None)
            what = "removed the statusLine key (there was none before)"
        write_settings(path, new_data, mtime)
        print(f"{what} in {path}")

    reg.pop("user", None)
    try:
        atomic_json(chm.REGISTRY_PATH, reg)
    except OSError as e:
        fail(f"settings restored but the registry {chm.REGISTRY_PATH} could not be "
             f"updated: {e}; hooks stay active until it is fixed")
    print(f"hooks are now inert; ledgers under {chm.SESSIONS_DIR} were kept")


def cmd_status(_args):
    reg = chm.load_registry()
    print(f"state dir: {chm.STATE_DIR}")
    print(f"plugin root: {reg.get('plugin_root') or '(unset)'}")
    print(f"launcher: {'present' if os.path.isfile(chm.LAUNCHER_PATH) else 'missing'}")
    entry = reg.get("user")
    if not entry:
        print("installed: no")
        return
    path = entry.get("settings_file", "?")
    try:
        with open(path, encoding="utf-8") as f:
            ours = is_ours(json.load(f).get("statusLine"))
        state = "statusLine is ours" if ours else "statusLine was changed by hand"
    except (OSError, ValueError):
        state = "settings file unreadable"
    print(f"installed: yes ({path}; {state})")


def main():
    ap = argparse.ArgumentParser(prog="setup.py", description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    sp = sub.add_parser("install")
    sp.add_argument("--plugin-root", help="plugin directory (default: this plugin)")
    sub.add_parser("remove")
    sub.add_parser("status")
    args = ap.parse_args()
    {"install": cmd_install, "remove": cmd_remove, "status": cmd_status}[args.cmd](args)


if __name__ == "__main__":
    main()
