---
name: brief-create
description: Creates a brief, the personal working file that carries one piece of work across sessions, at .briefs-local/<name>.md, or the checked-in folder the repo's CLAUDE.md names, through a short interview, then decisions, then the file. Creates only and never starts the work. Use when the user wants a brief or invokes /alt:brief-create.
argument-hint: [short name or the idea]
---

# brief-create

A brief is the plan and the handoff in one file. It belongs to the person doing the work, stays out of git unless this repo says otherwise, and is what a fresh session loads to pick the work back up. Create it, then stop.

## Inputs

The seed is $ARGUMENTS or whatever is in the conversation: an idea, a ticket key, a pasted story, the conversation so far. Read the ticket when a key and a tracker connection exist. Never ask what the conversation already answered.

Read if present, ignore if absent: an `## alt` section in the repo's CLAUDE.md, every line optional. `Tracker:` where tickets live and how to reach them. `Docs:` where the docs live. `Briefs:` a checked-in folder for briefs. `Phase closes when:` the proof command or the review that counts here. `Every brief loads:` what every brief here points at. A line absent is a default: the tracker tool the session reaches, README and `docs/`, `.briefs-local/`, a check written from the interview, nothing extra loaded.

## Where a brief lives

The briefs folder is `.briefs-local/` unless the `Briefs:` line is set; then it is that folder and the brief is committed with the work. A brief is `<folder>/<kebab-name>.md`; a finished one moves to `<folder>/closed/`. With `.briefs-local/` in a git repo, add `.briefs-local/` to `.gitignore` when the line is absent, then confirm with `git check-ignore -q .briefs-local/` before writing; if the check fails, say so, name the line, and stop. Without git, write.

One brief per piece of work, as many briefs as there is work. Never a brief about a brief.

## Ask what the template needs

One question a turn, and only for what the conversation, the ticket, and the code do not answer. Facts are looked up and cited in a few words. In order: goal, problem, who this is for and what changes for them, how we would know, done when, constraints, story, branches. Then propose the phases as units of change grouped in dependency order, from what was said and what the code shows, and let the user adjust. Stop asking when every section can be filled.

## Then decisions

Invoke `alt:decisions` against the drafted answers. Ask the user each root, one a turn. An answer folds into the sections above; `team` or no answer lands under Open Questions as one line with its role and if-wrong, the Dissolves sub-lines dropped. If decisions did not load, Open Questions reads `decisions did not run; run /alt:decisions on this brief` and the closing line says so.

## Write

Read `${CLAUDE_PLUGIN_ROOT}/skills/brief-create/template.md` only now. Fill it: the `Phase closes when` line becomes each phase's own check item and the `Every brief loads` line joins each phase's Load line, neither reworded. Write the file. Read it back: every phase ends with its close items, Story and Branches are filled or read none, no section the interview filled is empty; Findings and Retro start empty. Report the path and two lines on what the brief is. Then stop.

## Rules

- Never start the work, never edit code, never enter plan mode.
- A phase is a unit of change, smaller than a session. A session may hold several; a large phase may outlive one.
- No parked briefs, no splitting, no stamps or hashes, no session log.
- Findings are pointers to their durable home, never the finding itself.
- What the whole repo knows lives in its CLAUDE.md, never restated in a brief; only the close and load lines are carried over.
- In anything written to the brief, a ticket, a comment, or a message, a person is a name or handle and a role is Product Owner, Tech Lead, Engineer, or Designer.

## When something is missing, say so in one line

- No `## alt` section: `.briefs-local/`, and each phase's check written from what the interview said.
- decisions did not load: the placeholder, and say so.
- Ignore check fails: stop and name the line to add.
- No git: write, and Branches reads none.
- `Briefs:` names a folder that does not exist: create it.
