---
name: story-refine
description: Creates a story in the tracker from an idea or a pasted draft, or refines an existing item into one, stripped to what changes the code, proves it, or stops a guess. Use when the user wants a story, ticket, or issue written or refined, or invokes /alt:story-refine.
argument-hint: [key, pasted story, or the idea]
---

# story-refine

A story is what a developer alone can build correctly from, with nobody to ask. Every line changes the code, proves it, or stops a guess. Refine it, show it, write it on the runner's go, then stop.

## Inputs

The seed is $ARGUMENTS or whatever is in the room: a key, a pasted story, an idea, the conversation so far. A key with a tracker connection means refine that item; anything else means create.

Preset: the `## Preset` heading of any `.agentic/alt/*/extend-skill.md`, else developer.

Read if present, ignore if absent: `.agentic/sources.md`, where this team's facts live.

## Homework

Facts are looked up, never asked, and each is cited in a few words.

- tracker: the item by key, its full thread, and the parent the field names. A question the thread answered is not open. Never search by text; offer the duplicate search in one line and run it only on a yes.
- code: the part the story names, one step out: what it calls, what calls it, the tests and fixtures beside it. Cases come from here; so do the numbers a check can run against.
- docs: what covers that part, from the sources file and the item's links.
- people: never asked.

## Ask

One question a turn, only for what the room, the thread, and the code do not answer. In order: whose need this is and what they can do once it lands, what is broken today and the stake, the goal behind the feature, the cases that change what gets built, the check for each claim that could be wrong, any constraint no case would surface. Stop asking when the shape can be filled. A check with no data to run it is an Open line, not a question.

## Then examine

Invoke `alt:examine` against the draft. Its Decided list folds into cases, checks, and constraints. Its team bullets go under Open with their hats and if-wrong lines. If examine did not load, Open reads `examine did not run; run /alt:examine on this story` and the closing line says so.

## Show, then write

Read `${CLAUDE_PLUGIN_ROOT}/skills/story-refine/template.md` only now. Fill it, then show:

- On create: the title, the parent key or none, and the description.
- On refine, item already in the shape: each section where the item and this run disagree, both sides quoted. An Open line the thread answered leaves Open, lands as a case, check, or constraint, and its question and answer become one comment.
- On refine, item not in the shape: the new description, and the original text verbatim as a comment.

Ask once whether to create or edit it. On yes, write the title and parent to their fields and the description as one block, then the comments, through whatever tracker the session reaches. Report the key. Then stop.

## Rules

- One yes per run covers the item and its comments together.
- A line already in the item stays unless the runner says otherwise.
- Never a metric, a size, a priority, a status, or a readiness verdict on the story.
- Never starts the work, never edits code, never enters plan mode.
- Non-interactive: show the draft and stop; the write needs the runner present.

## When something is missing, say so in one line

- Nothing in the room: ask what the story is about, once.
- Key given, no tracker connection: create from what is in the room; the key is carried, the item unread.
- No tracker reachable at write time: the description in the room as markdown, and say the write was skipped.
- Item already complete: nothing to do.
- examine did not load: the placeholder, and say so.
- Preset is business or research: developer work only, for now.
