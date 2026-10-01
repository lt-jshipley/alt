---
name: sources-sync
description: Drafts or refreshes .agentic/sources.md, the one-page file that tells every alt skill where this team's facts live: code, docs, tracker, record, measures, people. Use when a repo is first wired to alt, when a source moves, or when the user invokes /alt:sources-sync.
---

# sources-sync

Every alt skill looks facts up before it asks. This file is where they look. It is the team's: one page, human-owned, committed.

## Seats

Six, and every fact has one.

- code: changes with the code. The repos.
- docs: changes with the business. `.docs/` unless the team keeps them elsewhere: a Confluence space, a wiki, `docs/`.
- tracker: changes as the work progresses. Jira, Issues, Boards.
- record: where a decision about a piece of work gets written. Usually the tracker item.
- measures: where this team's numbers live and who can pull one. Analytics, a dashboard, a report, a query. Epic-refine reads it for a baseline; no tool fills it by default.
- people: who holds what nothing else does.

Paths, counts, verdicts, and anything restating another seat live nowhere. Secrets are never a seat.

## Survey

Read `.agentic/sources.md` in the working directory if present. Then look at the folder: `.git` and its remotes; `.docs/` or `docs/`; a CLAUDE.md; the record heading of the preset this repo names (`## Preset` in any `.agentic/alt/*/extend-skill.md`, else developer). Each seat the file or the folder answers gets a draft line and its source in two words; the rest read "not seen". Nothing outside the folder places a seat: not a tool the session can reach, not a key in a commit message.

## Ask

When any seat reads "not seen", the first question is which tools this team uses: GitHub, Atlassian, Azure DevOps, or name them. Each named tool fills the seats it speaks to from `stacks.md`. Then one question a turn for any seat still empty.

## Write

Read `${CLAUDE_PLUGIN_ROOT}/skills/sources-sync/template.md` and `stacks.md` beside it only now. Fill each seat from the folder first, then the named tools, then the answers. Show the filled file. On the runner's go, write `.agentic/sources.md`, creating `.agentic/` when absent. When a file already exists, show each seat where the file and what this run learned disagree, both sides quoted, and change a line only on a yes. A default from `stacks.md` is never a disagreement. Then stop.

## Rules

- Never invents a place. A seat nothing answered reads "not set" and carries the question.
- Never assumes how repos relate. Parent, child, sibling, workspace: the team writes it under code.
- Writes one file. No CLAUDE.md line, no `.docs/` scaffold, no settings.
- Non-interactive: report and stop; write only when the prompt asked for it.

## When something is missing, say so in one line

- A named tool with no block in `stacks.md`: ask its seats one at a time, like any other answer.
- `.agentic` exists and is not a folder: stop and name it.
- The existing file has a heading the template lacks: keep it and report it.
