---
name: orient
description: Orients the session in the work it is about to do. Takes a brief, story key, branch, or a sentence and reports the system that work sits in. Reads only. Use when the user asks to orient or invokes /alt:orient.
argument-hint: [brief name, story key, branch, or the work in a sentence]
---

# orient

Give the session an understanding of the system it is about to work in. The intent names the work and `.agentic/sources.md` says where the facts live.

## The work

$ARGUMENTS names it: a brief in `.agentic/briefs/`, a story key, a branch, or a sentence. Bare means the standing brief: the one whose file name matches the current branch, else the one brief that reads `**Status:** Active`. A brief's Story and Branches lines name its story and branches; a story or branch names the brief whose line carries it, when one does. Never ask what the room already answered.

## Collect from the seats

Read `.agentic/sources.md` if present. The work opens one seat; the others are read where they join it, and no further.

- tracker: the one item by key. Title, status, owner, description, and the thread items nobody answered. Never an epic's children.
- record: decisions written about this work, wherever record points. Usually the same thread.
- code: the part of the system the work touches. Start from what the brief's Load line, the ticket, and the branch's touched files name, then one step out: the folders or modules around it, the entry points, the tests beside it, what it calls and what calls it. Names and signatures, never a sweep. With a branch, its distance from its base and the working tree.
- docs: what covers that part of the system, from the Load line, the ticket's links, and the docs seat's index when it has one.
- people: never asked.

Then the brief in full when there is one; the current phase is the first with an unchecked item. Kind is the brief's `**Kind:**` line, else `## Preset` in any `.agentic/alt/*/extend-skill.md`, else developer.

## Report

```
<the work>: <Status and phase when a brief; the story's status when a story>
<where the work stands, in a paragraph>

The system it touches
- <area>: <landmarks, what it connects to, the conventions seen>

Open in this phase
- [ ] <item>

Open questions
- <line from the brief>

Disagreements
- <source A> says <quoted>; <source B> says <quoted>

Read: <what was read>. Absent: <what was not, each named once>.
What next?
```

Disagreements holds two checks and nothing else: the brief's Status against the tracker's, and its Branches against git. Raw facts, no verdicts; what else the sources show goes in the paragraph or nowhere. When Open questions has a line, recommend `/alt:examine` in one sentence; with no brief, recommend `/alt:brief-create`. Never invoke either. Then stop.

## Rules

- Writes nothing, starts nothing, never enters plan mode.
- Stop reading when the report can be written.
- Kind is read, never inferred from the folder.
- No free-text search of the tracker unless asked; offer it in one line.
- Non-interactive: report on what the intent settles and stop.

## When something is missing, say so in one line

- Nothing named and no standing brief: ask what work to orient in.
- No `.agentic/sources.md`: the preset's record heading and the folder.
- Preset cannot be read: developer's words.
- A seat the file lists but this session cannot reach: its Ask hat, as a look-this-up line.
- A seat the file does not list: skipped, unmentioned.
- A key with no tracker connection: the key is carried, the item unread.
- No git: the branch checks are skipped.
- A brief with no Status or Kind line: reported as unknown, never skipped.
