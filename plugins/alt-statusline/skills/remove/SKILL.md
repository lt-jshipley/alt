---
name: remove
description: Uninstall the alt-statusline gauge. Restores the previous statusLine setting and switches the hooks off. Use only when the user asks to remove, uninstall, or disable alt-statusline.
disable-model-invocation: true
allowed-tools:
  - Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/setup.py" *)
---

# remove

## Check, then run

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/setup.py" status
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/setup.py" remove
```

If status says it is not installed, say so and stop. Otherwise relay the remove output verbatim and say what was restored. Session ledgers are kept; mention that only if asked. Then stop.
