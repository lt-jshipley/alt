---
name: remove
description: Uninstall the alt-statusline gauge. Restores the previous statusLine setting and switches the hooks off for this user or a folder. Use only when the user asks to remove, uninstall, or disable alt-statusline.
argument-hint: [user|folder]
disable-model-invocation: true
allowed-tools:
  - Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/setup.py" *)
---

# remove

## Find what is installed

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/setup.py" status
```

If `$ARGUMENTS` is `user` or `folder`, use it. Otherwise: one scope installed, use that; both installed, ask which, or both; none, say so and stop.

## Run

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/setup.py" remove --scope <scope> --folder "${CLAUDE_PROJECT_DIR}"
```

For a folder other than this one, pass its path from the status output as `--folder`.

Relay the output verbatim and say what was restored. Session ledgers are kept; mention that only if asked. Then stop.
