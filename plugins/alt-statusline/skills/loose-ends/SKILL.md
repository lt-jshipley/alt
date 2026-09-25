---
name: loose-ends
description: Lists this session's loose ends, the approaches and questions the gauge saw start and never saw finish, says what became of each from the session's own memory, and closes the ones the user confirms. Use when the user asks about loose ends, wants to wrap them up, asks why the gauge says loose ends, or invokes /alt-statusline:loose-ends.
allowed-tools:
  - Bash(python3 "${CLAUDE_PLUGIN_ROOT}/scripts/loose_ends.py" *)
---

# loose-ends

A loose end is something this session started and never said it finished. The gauge counts them; this skill settles them. Closing is a write to the session's ledger, so the gauge changes on its next render.

## List

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/loose_ends.py" list
```

If it says not installed, no session id, or no loose ends, relay the line and stop.

## Read each one

For every numbered entry, one line from this session's own memory, in this form:

- `<n>. done: <what settled it, a few words>`
- `<n>. dropped: <why, a few words>`
- `<n>. still open`

Never invent an outcome. Unsure means still open. The judge that wrote the entry saw only one turn at a time; this session saw all of them, so its reading wins, but only where it remembers.

## Close

Ask once: close the done and dropped ones, numbers listed? On a yes, or an edited set of numbers:

```
python3 "${CLAUDE_PLUGIN_ROOT}/scripts/loose_ends.py" close <n> [<n>...]
```

Relay its output verbatim. If it says the judge is still grading, say so and offer to try again; run it once more only when asked.

What stays open is named in one line, nothing more. This skill never starts that work. Then stop.

## Non-interactive

List and the per-entry reading only. Close nothing.
