---
name: story-refine
description: Creates a story in the tracker from an idea or a pasted draft, or refines an existing item into one, stripped to what the system will do, what proves it, and what stops a guess, never how. Use when the user wants a story, ticket, or issue written or refined, or invokes /alt:story-refine.
argument-hint: [key, pasted story, or the idea]
---

# story-refine

A story is what a developer alone can build correctly from, with nobody to ask. Every line says what the system will do for whom, proves it where the person sees it, or stops a guess; none says how. Refine it, show it, write it on the runner's go, then stop.

## Inputs

The seed is $ARGUMENTS or whatever is in the room: a key, a pasted story, an idea, the conversation so far. A key with a tracker connection means refine that item; anything else means create.

Preset: the `## Preset` heading of any `.agentic/alt/*/extend-skill.md`, else developer.

Read if present, ignore if absent: `.agentic/sources.md`, where this team's facts live, and `.agentic/alt/story-refine/extend-skill.md`, this repo's overrides under two headings. `## Preset`: one word. `## Shows`: the fields the product shows a person, which every case names as final wording or the boundary line covers.

## Homework

Facts are looked up, never asked, and each is cited in the room by path and a symbol, heading, or quoted phrase, never a bare line number. That form is for the room; nothing written to the tracker cites a source file.

- tracker: the item by key, its full thread, and the parent the field names. A question the thread answered is not open. Never search by text; offer the duplicate search in one line and run it only on a yes.
- code: the part the story names, one step out: what it calls, what calls it, the tests and fixtures beside it. Cases come from here; so do the numbers a check can run against.
- docs: what covers that part, from the sources file and the item's links, what the product itself says about it, and the file that defines the product's words when the repo has one; cases are written in them, and a word the cases need that it lacks is either the how or a term the repo should define.
- people: never asked.

The homework shapes the cases and catches false premises; none of it is written into the story. A fact a case rests on is stated at the product level in the case, and goes to a comment only when a reader might dispute it.

## Ask

One question a turn, only for what the room, the thread, and the code do not answer. In order: whose need this is and what they can do once it lands, what is broken today and the stake, the goal behind the feature when there is no parent to read it from, the cases that change what gets built, the check for each claim that could be wrong, any constraint no case would surface. Stop asking when the shape can be filled. A check with no data to run it is an Open line, not a question.

## Then decisions

Invoke `alt:decisions` against the draft. Ask the runner each root, one a turn. An answer folds into cases, checks, and constraints; `team` or no answer lands under Open with its hat and if-wrong line. When those lines are about the need, the outcome, or the why rather than the cases, one `Parent:` line under Open says so and names the parent key or `none`; they are the epic's questions surfacing here. An answer about the how, which helper, where the code lives, is said in the room and not written into the story; when it binds more than one story it is an ADR or the parent's constraint, and the story cites it. If decisions did not load, Open reads `decisions did not run; run /alt:decisions on this story` and the closing line says so.

## Show, then write

Read `${CLAUDE_PLUGIN_ROOT}/skills/story-refine/template.md` only now. Fill it, then show:

- On create: the title, the parent key or none, and the description.
- On refine, item already in the shape: each section where the item and this run disagree, both sides quoted. An Open line the thread answered leaves Open, lands as a case, check, or constraint, and its question and answer become one comment. A Code section, or any line naming a file, symbol, helper, sibling, fixture, or test, is shown as a disagreement with its replacement: the outcome it protected as a case or constraint, or nothing.
- On refine, item not in the shape: the new description, and the original text verbatim as a comment.

Ask once whether to create or edit it. On yes, write the title and parent to their fields and the description as one block, then the comments, through whatever tracker the session reaches. Report the key. Then stop.

## Rules

- One yes per run covers the item and its comments together.
- A line already in the item stays unless the runner says otherwise.
- Never a metric, a size, a priority, a status, or a readiness verdict on the story.
- Never starts the work, never edits code, never enters plan mode.
- Never a file, symbol, helper, sibling, fixture, or test name in the story; a path only as the source of a constraint.
- Written outside the session, to a tracker item, a comment, or a message, a person is a name or handle and a role is the preset's word. The words the skills use for their own mechanics, runner, room, seat, hat, wound, shape, the record, never appear there.
- Non-interactive: every root lands under Open; show the draft and stop; the write needs the runner present.

## When something is missing, say so in one line

- Nothing in the room: ask what the story is about, once.
- Key given, no tracker connection: create from what is in the room; the key is carried, the item unread.
- No tracker reachable at write time: the description in the room as markdown, and say the write was skipped.
- Item already complete: nothing to do.
- decisions did not load: the placeholder, and say so.
- Preset is business or research: developer work only, for now.
