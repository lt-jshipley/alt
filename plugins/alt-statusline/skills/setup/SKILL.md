---
name: setup
description: Install the alt-statusline gauge for this user. Replaces the current statusLine setting, keeps a backup for /alt-statusline:remove, and switches the hooks on. Use only when the user asks to set up, install, or enable alt-statusline.
disable-model-invocation: true
allowed-tools:
  - Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/setup.py" *)
---

# setup

Installs the gauge for every session on this machine. Nothing in this plugin runs until this has been done once. It writes `statusLine` into `~/.claude/settings.json`.

## Run

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/setup.py" install --plugin-root "${CLAUDE_PLUGIN_ROOT}"
```

Relay its output verbatim, warnings included. It refuses with one line saying why when `claude` or `python3` is missing from PATH, the state directory is not writable, or the settings file is not valid JSON. On a refusal, stop. Never edit settings by hand.

## After a successful install, say

- The statusline appears as soon as the settings file is saved. No restart.
- The hooks are live from the next event; the plugin is already loaded.
- The previous statusline setting is backed up; `/alt-statusline:remove` restores it.
- To keep the gauge but skip the per-turn model call in one project, set `CHM_NO_JUDGE` to `1` in that project's settings `env` block.

Then stop.
