#!/usr/bin/env python3
"""alt-statusline launcher — the stable file the statusLine setting points at.

Plugin installs live in a versioned cache directory that changes on every
update, so settings must never point into the plugin. setup.py copies this
file into the state dir (next to install.json). It reads the session JSON
from stdin, resolves the plugin root that session started with — stamped into
its ledger by the SessionStart hook — and runs that plugin's statusline.py
with the same stdin. Fallbacks: the registry's plugin_root (last session to
start), then the newest cached copy.

The statusline runs as a child rather than an exec: stdin has been consumed
to find the session, and re-feeding it through a pipe hangs on payloads over
64KB. Failure is quiet by design: with no plugin to be found it prints one
dim line and exits 0, so a stale setting never errors on every render.
"""

import glob
import json
import os
import subprocess
import sys

STATE_DIR = os.path.dirname(os.path.abspath(__file__))
SESSIONS_DIR = os.path.join(STATE_DIR, "sessions")
REGISTRY = os.path.join(STATE_DIR, "install.json")
CACHE_GLOB = os.path.expanduser(
    "~/.claude/plugins/cache/*/alt-statusline/*/scripts/statusline.py")
DIM, RESET = "\033[2m", "\033[0m"
NOT_FOUND = (f"{DIM}alt-statusline: plugin not found; "
             f"run /alt-statusline:remove or reinstall{RESET}")


def read_stdin():
    try:
        if sys.stdin.isatty():
            return b"{}"
        return sys.stdin.buffer.read() or b"{}"
    except (OSError, ValueError):
        return b"{}"


def session_id(raw):
    try:
        sid = json.loads(raw).get("session_id")
    except (ValueError, AttributeError):
        return ""
    if not isinstance(sid, str) or "/" in sid or sid in (".", ".."):
        return ""
    return sid


def json_field(path, key):
    try:
        with open(path) as f:
            return json.load(f).get(key)
    except (OSError, ValueError, AttributeError):
        return None


def candidates(sid):
    if sid:  # the plugin this session started with
        root = json_field(os.path.join(SESSIONS_DIR, f"{sid}.json"), "plugin_root")
        if root:
            yield os.path.join(root, "scripts", "statusline.py")
    root = json_field(REGISTRY, "plugin_root")  # last session to start
    if root:
        yield os.path.join(root, "scripts", "statusline.py")
    found = []  # newest cached copy; a dir can vanish mid-render on update
    for path in glob.glob(CACHE_GLOB):
        try:
            found.append((os.path.getmtime(path), path))
        except OSError:
            pass
    for _, path in sorted(found, reverse=True):
        yield path


def main():
    raw = read_stdin()
    for target in candidates(session_id(raw)):
        if not os.path.isfile(target):
            continue
        env = dict(os.environ, CHM_STATE_DIR=STATE_DIR)  # this dir is the install
        try:
            return subprocess.run([sys.executable, target], input=raw, env=env).returncode
        except OSError as e:
            print(f"{DIM}alt-statusline: cannot run {target}: {e}{RESET}")
            return 0
    print(NOT_FOUND)
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:  # never error on every render
        print(f"{DIM}alt-statusline: launcher failed: {e}{RESET}")
        sys.exit(0)
