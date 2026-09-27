---
name: epic-create
description: Creates an epic in the tracker from an idea, a handed-down feature, a pasted thread, or an existing item, written from the business side without reading source code, so the person who decides go or no-go can sign it and the team that will slice it can challenge it, saying whose need it is in their words, how we will know, what we are betting on and the evidence, what was decided and why, and what is open and whose, never how and never a feature as the need. Never creates the stories under it. Use when the user wants an epic written from the business side, says "epic-create", or invokes /alt:epic-create.
argument-hint: [key, pasted epic or thread, or the idea]
---

# epic-create

An epic is a bet written down, by the business side, so the person who decides go or no-go can sign it and the team that will slice it can challenge it. Every line names the need, says how we will know, names what we are betting on, records a choice and why, or names a question and whose it is. None says how, and none carries a feature as the need: a need only one solution could meet is a solution in disguise, and the solution goes to the Bet as a guess. The skill never reads source code and never proposes a number. Draft it, have it reviewed, show it, write it on the runner's go, then stop.

## Inputs

The seed is $ARGUMENTS or whatever is in the room: a key, a pasted epic or thread, a feature someone asked for, the conversation so far. A key with a tracker connection means rewrite that item; anything else means create.

Read if present, ignore if absent: `.agentic/sources.md`, where this team's facts live, its `## measures` seat in particular. An assistant in the seed is never an owner and never a source of a decision; its proposals are questions only where a person in the seed took them up.

## Homework

Facts are looked up, never asked, and each is cited in the room by path and a heading or quoted phrase. That form is for the room; nothing written to the tracker cites a source.

- tracker: the item by key, its full thread, the parent the field names and its Outcome line, and each child's title, status, and parent link, never a child's body; with no parent, the open items the seed or the thread links. A question a thread answered is not open. Never search by text; offer the duplicate search in one line and run it only on a yes.
- product: what the product itself says and shows about this, and the file that defines the product's words when the repo has one. The epic is written in those words.
- measures: the baseline for the outcome, from the seat, cited in the room. No seat, or no number in it, is the unmeasured line.
- code: never. Feasibility is a Bet line with its evidence, and what the builder finds in the code comes back later as questions.
- people: never asked, except the target, which is asked of whoever holds the measure and never proposed.

The homework shapes the epic; none of it is written into the epic or beside it.

## Ask

One question a turn, only for what the room and the thread do not answer. In order: what the people who asked for this would do differently once it lands, and what that does for the business; who they are, plural and specific; who decides go or no-go; who holds the measure; the target, asked of the measure holder; roof shot or moon shot, only if they say. A feature handed down is converted by the first question and never carried as the need. Stop asking when the shape can be filled. A question with nobody in the room to answer it is an Open line, unassigned. A way of building that someone in the thread proposed is the Bet's guess or a story's question, never the need and never a rule. A proposal the thread turned down is a Decided line, with the reason given. Small enough to be a story: say so, name `alt:story-create`, stop. A level above an epic: say so, stop. When the thread says the epic should not exist, the draft says so in one line with who decides, and the write is offered anyway.

## Fill

Read `${CLAUDE_PLUGIN_ROOT}/skills/epic-create/template.md` only now and fill it. A fourth line in any section is offered to the runner in one line with what it protects, written on a yes, dropped otherwise. A section that wants a fifth is an epic that wants splitting, and the split is named in the room. A number slot with nothing in the seed or the measures seat is the unmeasured line.

## Before showing

Write the draft to a file under the session's scratch space, the seed beside it, and run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/epic-create/scripts/check.py <draft> <seed>`. Fix each line it prints and run it again. Then send the draft and the seed in full, never a summary, to a sub-agent that has read neither, with one instruction: invoke `alt:epic-review` against them, and a list of the product's words the draft uses, which the review never cuts for being absent from the seed. Take its edited draft as the draft. Its Changed and Could not fix lines are shown beside the draft; a Could not fix line the runner cannot settle becomes an Open line.

## Show, then write

Show:

- On create: the title, the parent key or none, and the description.
- On rewrite, item already in the shape: each section where the item and this run disagree, both sides quoted; a line already there stays unless the runner says otherwise. An Open line the thread answered leaves Open and lands where its answer belongs.
- On rewrite, item not in the shape: a create from the need the item names; nothing in it is kept for being there, and the original stays in the item's edit history.

Then, in the room only: the Open lines, since the epic is not ready to slice until they close; one line saying no-go is an allowed answer and who gives it; and one line saying the builder's pass against the code comes next and returns questions, not text.

Ask once whether to create or edit it. On yes, write the title and parent to their fields and the description as one block, through whatever tracker the session reaches. Report the key. Then stop.

## Rules

- Never a target the team did not set, a confidence word or number, a size, a priority, a status, a date, or a readiness verdict on the epic. Never a sentence telling the reader the epic may be wrong.
- Never creates, edits, links, or moves a child. Never a line that lists children; they are the tracker's links.
- Nothing sits beside the epic: no comment, no second document. A link the seed already holds may sit on an Evidence line.
- Never starts the work, never edits code, never enters plan mode.
- Written outside the session, to a tracker item or a message, a person is a name or handle and a role is a plain word anyone on the team would use. The words the skills use for their own mechanics, runner, room, shape, the record, never appear there.
- Non-interactive: show the draft and stop; the write needs the runner present.

## When something is missing, say so in one line

- Nothing in the room: ask what the need is, once.
- Key given, no tracker connection: create from what is in the room; the key is carried, the item unread.
- No tracker reachable at write time: the description in the room as markdown, and say the write was skipped.
- Measures seat absent from the sources file: say `sources file has no measures seat; run /alt:sources-sync when a number exists`, once, and write the unmeasured line. Seat empty: the unmeasured line only.
- Item already complete: nothing to do.
