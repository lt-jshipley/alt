---
name: sources-sync
description: Drafts or refreshes .agentic/sources.md, the one-page file that tells every alt skill where this team's facts live: code, docs, tracker, record, people. Reads the folder and the session's tools, asks only what it cannot see, writes on the runner's go. Use when a repo is first wired to alt, when a source moves, or when the user invokes /alt:sources-sync.
---

# sources-sync

Every alt skill looks facts up before it asks. This file is where they look. It is the team's: one page, human-owned, committed. This skill drafts it from what is in the room and decides nothing for the team.

## Seats

Five, and every fact has one.

- code: changes with the code. The repos.
- docs: changes with the business. `.docs/` unless the team keeps them elsewhere: a Confluence space, a wiki, `docs/`.
- tracker: changes as the work progresses. Jira, Issues, Boards.
- record: where a decision about a piece of work gets written. Usually the tracker item.
- people: who holds what nothing else does.

Paths, counts, verdicts, and anything restating another seat live nowhere. Secrets are never a seat.

## Survey

Read `.agentic/sources.md` in the working directory if present. Then look: `.git` and its remotes; `.docs/` or `docs/`; a CLAUDE.md; an Atlassian, GitHub, or Azure DevOps tool the session can reach; a tracker key in recent commit messages; the record heading of the preset this repo names (`## Preset` in any `.agentic/alt/*/extend-skill.md`, else developer). Each seat gets a draft line and its source in two words, or "not seen".

## Ask

One question a turn, only for a seat nothing answered. Never ask what the folder shows. Zero questions is a success.

## Write

Read `${CLAUDE_PLUGIN_ROOT}/skills/sources-sync/template.md` only now. Show the filled file. On the runner's go, write `.agentic/sources.md`, creating `.agentic/` when absent. When a file already exists, show each seat where the file and the folder disagree, both sides quoted, and change a line only on a yes. Then stop.

## Rules

- Never invents a place. A seat nothing answered reads "not set" and carries the question.
- Never assumes how repos relate. Parent, child, sibling, workspace: the team writes it under code.
- Writes one file. No CLAUDE.md line, no `.docs/` scaffold, no settings.
- Non-interactive: report and stop; write only when the prompt asked for it.

## When something is missing, say so in one line

- No git, no tools, no docs folder: five "not set" seats and one question, what do you use.
- `.agentic` exists and is not a folder: stop and name it.
- The existing file has a heading the template lacks: keep it and report it.
