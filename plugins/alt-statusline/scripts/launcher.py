#!/usr/bin/env python3
"""alt-statusline launcher — the stable file the statusLine setting points at.

Plugin installs live in a versioned cache directory that changes on every
update, so settings must never point into the plugin. setup.py copies this
file into the state dir (next to install.json); it looks up the current
plugin root and execs the real statusline from there with stdin intact.

Failure is quiet by design: with no plugin to be found it prints one dim line
and exits 0, so a stale setting never errors on every render.
"""

import glob
import json
import os
import sys

STATE_DIR = os.path.dirname(os.path.abspath(__file__))
REGISTRY = os.path.join(STATE_DIR, "install.json")
CACHE_GLOB = os.path.expanduser(
    "~/.claude/plugins/cache/*/alt-statusline/*/scripts/statusline.py")
DIM, RESET = "\033[2m", "\033[0m"


def candidates():
    try:
        with open(REGISTRY) as f:
            root = json.load(f).get("plugin_root")
        if root:
            yield os.path.join(root, "scripts", "statusline.py")
    except (OSError, ValueError, AttributeError):
        pass
    # registry stale (plugin updated, no session started yet): newest cached copy
    found = glob.glob(CACHE_GLOB)
    found.sort(key=os.path.getmtime, reverse=True)
    for path in found:
        yield path


for target in candidates():
    if os.path.isfile(target):
        env = dict(os.environ, CHM_STATE_DIR=STATE_DIR)  # this dir is the install
        os.execve(sys.executable, [sys.executable, target], env)

print(f"{DIM}alt-statusline: plugin not found; run /alt-statusline:remove or reinstall{RESET}")
