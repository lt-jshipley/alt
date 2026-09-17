---
name: brief-create
description: Creates a brief, the personal working file that carries one piece of work across sessions, at .agentic/briefs/<name>.md, through a short interview, then examine, then the file. Creates only and never starts the work. Use when the user wants a brief or invokes /alt:brief-create.
argument-hint: [preset] [short name or the idea]
---

# brief-create

A brief is the plan and the handoff in one file. It belongs to the person doing the work, is never committed, and is what a fresh session loads to pick the work back up. Create it, then stop.

## Inputs

The seed is $ARGUMENTS or whatever is in the room: an idea, a ticket key, a pasted story, the conversation so far. Read the ticket when a key and a tracker connection exist. Never ask what the room already answered.

Preset: the first word of $ARGUMENTS if it names a file in `${CLAUDE_PLUGIN_ROOT}/presets/`, else the `## Preset` heading of the extension file, else `developer.md`. Drop the word from the seed. The preset names the kind of work and supplies its words.

Read if present, ignore if absent: `.agentic/sources.md`, where this team's facts live, and `.agentic/alt/brief-create/extend-skill.md`, this repo's overrides under three headings. `## Preset`: one word, developer, business, or research. `## Close`: what closes a phase here, the proof command or the review that counts. `## Load`: what every brief here points at. An empty heading is the same as an absent one.

## Where a brief lives

`.agentic/briefs/<kebab-name>.md`. A finished brief moves to `.agentic/briefs/closed/`. In a git repo, add `.agentic/briefs/` to `.gitignore` when the line is absent, then confirm with `git check-ignore -q .agentic/briefs/` before writing; if the check fails, say so, name the line, and stop. `.agentic/` itself stays committed. Without git, write.

One brief per piece of work, as many briefs as there is work. Never a brief about a brief.

## Ask what the template needs

One question a turn, and only for what the room, the record, and the code do not answer. Facts are looked up and cited in a few words. In order: goal, problem, who this is for and what changes for them, how we would know, done when, constraints, story, branches. Then propose the phases as units of change grouped in dependency order, from what was said and what the code shows, and let the runner adjust. Stop asking when every section can be filled.

## Then examine

Invoke `alt:examine` against the drafted answers. Its Decided list folds into the sections above. Its team bullets and anything still open go under Open Questions with their if-wrong lines. If examine did not load, Open Questions reads `examine did not run; run /alt:examine on this brief` and the closing line says so.

## Write

Read `${CLAUDE_PLUGIN_ROOT}/skills/brief-create/template.md` only now. Fill it and write the file. Read it back: every phase ends with its close items, Story and Branches are filled or read none, no section is empty. Report the path and two lines on what the brief is. Then stop.

## Rules

- Never start the work, never edit code, never enter plan mode.
- A phase is a unit of change, smaller than a session. A session may hold several; a large phase may outlive one.
- No parked briefs, no splitting, no stamps or hashes, no session log.
- Findings are pointers to their durable home, never the finding itself.
- What only this repo knows lives in the extension file and is never copied into the template's sections.

## When something is missing, say so in one line

- Preset cannot be read: ask which kind of work this is.
- Extension file absent: developer, and the template's generic close item.
- examine did not load: the placeholder, and say so.
- Ignore check fails: stop and name the line to add.
- No git: write, and Branches reads none.
