---
name: setup
description: Install the alt-statusline gauge for this user or for the current folder. Replaces the current statusLine setting, keeps a backup for /alt-statusline:remove, and switches the hooks on. Use only when the user asks to set up, install, or enable alt-statusline.
argument-hint: [user|folder]
disable-model-invocation: true
allowed-tools:
  - Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/setup.py" *)
---

# setup

Installs the gauge. Nothing in this plugin runs until this has been done once.

## Scope

If `$ARGUMENTS` is `user` or `folder`, use it. Otherwise ask one question and wait for the answer:

- **user**: every session on this machine. Writes `~/.claude/settings.json`.
- **folder**: only sessions launched in this repository. Writes `.claude/settings.local.json` at the repository root, which stays personal to this machine.

## Run

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/setup.py" install --scope <scope> --folder "${CLAUDE_PROJECT_DIR}" --plugin-root "${CLAUDE_PLUGIN_ROOT}"
```

Relay its output verbatim, warnings included. It refuses with one line saying why when `claude` or `python3` is missing from PATH, the state directory is not writable, or the settings file is not valid JSON. On a refusal, stop. Never edit settings by hand.

## After a successful install, say

- The statusline appears as soon as the settings file is saved. No restart.
- The hooks are live from the next event; the plugin is already loaded.
- In a folder Claude Code has not trusted yet, the statusline stays blank until the trust dialog is accepted.
- The previous statusline setting is backed up; `/alt-statusline:remove` restores it.

Then stop.
