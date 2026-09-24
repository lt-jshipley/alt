---
name: epic-refine
description: Creates an epic in the tracker from an idea, a handed-down feature, or a pasted draft, or refines an existing one into a need with an outcome, a bet, and who holds each. Never creates the stories under it. Use when the user wants an epic written or refined, or invokes /alt:epic-refine.
argument-hint: [key, pasted epic, or the idea]
---

# epic-refine

An epic is a bet written down. Every line decides what gets built, says how we will know, names what we are betting on, or says who holds it. Refine it, show it, write it on the runner's go, then stop.

## Inputs

The seed is $ARGUMENTS or whatever is in the room: a key, a pasted epic, a feature someone asked for, the conversation so far. A key with a tracker connection means refine that item; anything else means create.

Preset: the `## Preset` heading of any `.agentic/alt/*/extend-skill.md`, else developer.

Read if present, ignore if absent: `.agentic/sources.md`, where this team's facts live, its `## measures` seat in particular.

## Homework

Facts are looked up, never asked, and each is cited in a few words.

- tracker: the item by key and its full thread; the parent the field names and its outcome line; each child's title, status, and parent link, never a child's body. A question the thread answered is not open. Never search by text; offer the duplicate search in one line and run it only on a yes.
- docs: what the item links and what the sources file names for this part.
- measures: the baseline for the outcome, from the seat.
- code: none, unless a Bet line needs a feasibility fact; then the one part it names, one step out, cited.
- people: never asked.

## Ask

One question a turn, only for what the room, the thread, and the sources do not answer. In order: what the people who asked for this would do once it lands, and what it would do for the business; who they are, plural and specific; who holds the need, the measure, and the decisions; the target, asked of whoever holds the measure. A feature is converted by the first question, never carried as the need. Stop asking when the shape can be filled.

## Then decisions

Invoke `alt:decisions` against the draft. Ask the runner each root, one a turn. An answer folds into the Bet, the Not line, and the constraint; `team` or no answer lands under Open with its hat, name when known, and if-wrong line. If decisions did not load, Open reads `decisions did not run; run /alt:decisions on this epic` and the closing line says so.

## Show, then write

Read `${CLAUDE_PLUGIN_ROOT}/skills/epic-refine/template.md` only now. Fill it, then show:

- On create: the title, the parent key or none, and the description.
- On refine, item already in the shape: each section where the item and this run disagree, both sides quoted. A `Not yet a story` line whose piece now has a child leaves the body. A child whose title does not serve the need is named in the room and becomes one Open line held by Tech Leadership.
- On refine, item not in the shape: the new title when the old one names a feature, the new description, and the original title and text verbatim as one comment.
- When the draft says the epic should not exist: say so in one line with who decides, and offer the write anyway.

Ask once whether to create or edit it. On yes, write the title and parent to their fields and the description as one block, then the comments, through whatever tracker the session reaches. Report the key. Then stop.

## Rules

- One yes per run covers the item and its comments together.
- A line already in the item stays unless the runner says otherwise.
- Never a target the team did not set, a confidence word or number, a size, a priority, a status, a date, or a readiness verdict on the epic.
- Never creates, edits, links, or moves a child.
- A field the sources file names is used and never restated in the description.
- Never starts the work, never edits code, never enters plan mode.
- Non-interactive: every root lands under Open; show the draft and stop; the write needs the runner present.

## When something is missing, say so in one line

- Nothing in the room: ask what the need is, once.
- Title only, no children: write the need if the room has it, else nothing to do.
- Small enough to be a story: say so, name story-refine, stop.
- A level above the epic: say so, stop.
- Key given, no tracker connection: create from what is in the room; the key is carried, the item unread.
- No tracker reachable at write time: the description in the room as markdown, and say the write was skipped.
- Measures seat absent from the sources file: say `sources file has no measures seat; run /alt:sources-sync when a number exists`, once, and write the unmeasured line. Seat empty: the unmeasured line only.
- Item already complete: nothing to do.
- Preset is business or research: developer work only, for now.
