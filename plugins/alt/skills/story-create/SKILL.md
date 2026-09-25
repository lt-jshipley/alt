---
name: story-create
description: Creates a story in the tracker from an idea, a pasted draft, or an existing item, written from the business side without reading source code, so a product owner can sign it and a builder can challenge it, saying what changes for whom, the rules it is accepted against, the examples at the edges, what was decided and why, and what is open and whose, never how. Use when the user wants a story written from the business side, says "story-create", or invokes /alt:story-create.
argument-hint: [key, pasted story, or the idea]
---

# story-create

A story is what a team agrees to build, written by the business side so the product owner can sign it and the builder can challenge it. Every line says what changes for whom, states a rule the signer would reject the work over, shows an example at an edge, records a choice and why, or names a question and whose it is. None says how, and no section holds what the story leaves out; a case it does not handle is an Open line if someone must decide it, and nothing otherwise. The test for every line is one: if only one way of building could satisfy it, it says how and goes. The skill never reads source code; what the builder finds there comes back later as questions, not as story text. Draft it, have it reviewed, show it, write it on the runner's go, then stop.

## Inputs

The seed is $ARGUMENTS or whatever is in the room: a key, a pasted story, an idea, the conversation so far. A key with a tracker connection means rewrite that item; anything else means create.

Read if present, ignore if absent: `.agentic/sources.md`, where this team's facts live, and `.agentic/alt/story-create/extend-skill.md`, this repo's one override under one heading, `## Shows`: the names of the fields the product shows a person as a headline, nothing else. Where the template and the extend file disagree, the template rules. An assistant in the seed is never an owner and never a source of a decision; its proposals are questions only where a person in the seed took them up.

## Homework

Facts are looked up, never asked, and each is cited in the room by path and a heading or quoted phrase. That form is for the room; nothing written to the tracker cites a source.

- tracker: the item by key, its full thread, the parent the field names, and the parent's other open children by title and Open section; with no parent, the open items the seed or the thread links. A question a thread answered is not open. A question two siblings both carry is one question, owned once, on the story whose change causes it. Never search by text; offer the duplicate search in one line and run it only on a yes.
- product: what the product itself says and shows about this, the report, the screen, the message, and the file that defines the product's words when the repo has one. The story is written in those words.
- code: never. Not the part the story names, not its tests, not its docs. Reading it puts one solution in the writer's head, and every line after is written against that solution.
- people: never asked.

The homework shapes the story; none of it is written into the story or beside it.

## Ask

One question a turn, only for what the room and the thread do not answer. In order: whose need this is, the person the product serves, and what they stop or start doing once it lands; what was seen, when, and in what words; the rules the product owner would reject the work over; the example at each edge the rules leave open; a choice made on the way and why. Stop asking when the shape can be filled. A question with nobody in the room to answer it is an Open line, not a question. A claim the thread leaves unchecked is an Open line, not an example. A way of building that someone in the thread proposed, or described as how it works today, is a question, not a rule, however settled it sounded. A proposal the thread turned down is a Decided line, with the reason given. With no parent, offer `alt:epic-refine` once before the write; a decline leaves the parent field empty with nothing said about why.

## Fill

Read `${CLAUDE_PLUGIN_ROOT}/skills/story-create/template.md` only now and fill it. The incident is the first example; a line where two rules meet comes before one that restates a rule. A fourth line in any section is offered to the runner in one line with what it protects, written on a yes, dropped otherwise. A section that wants a fifth is a story that wants splitting, and the split is named in the room.

## Before showing

Write the draft to a file under the session's scratch space and run `python3 ${CLAUDE_PLUGIN_ROOT}/skills/story-create/scripts/check.py <file>`. Fix each line it prints and run it again. Then send the draft and the seed to a sub-agent that has read neither, with one instruction: invoke `alt:story-review` against them. Take its edited draft as the draft. Its Changed and Could not fix lines are shown beside the draft; a Could not fix line the runner cannot settle becomes an Open line.

## Show, then write

Show:

- On create: the title, the parent key or none, the keys it waits on, and the description.
- On rewrite, item already in the shape: each section where the item and this run disagree, both sides quoted; a line already there stays unless the runner says otherwise. An Open line the thread answered leaves Open and lands where its answer belongs.
- On rewrite, item not in the shape: a create from the need the item names; nothing in it is kept for being there, and the original stays in the item's edit history.

Then, in the room only, the Open lines that change what the person sees, since the story is not ready to pull until they close, and one line saying the builder's pass against the code comes next and returns questions, not text.

Ask once whether to create or edit it. On yes, write the title and parent to their fields, the description as one block, and each item this story waits on as the tracker's dependency relation, through whatever tracker the session reaches. A dependency the relation cannot hold, a pull request or a branch, is said in the room and written nowhere. Report the key. Then stop.

## Rules

- A line that changes what the person sees is a criterion or an example, wherever it started.
- Never a metric, a size, a priority, a status, or a readiness verdict on the story. Never a sentence telling the reader the story may be wrong.
- Never starts the work, never edits code, never enters plan mode.
- Written outside the session, to a tracker item or a message, a person is a name or handle and a role is a plain word anyone on the team would use. The words the skills use for their own mechanics, runner, room, shape, the record, never appear there.
- Non-interactive: show the draft and stop; the write needs the runner present.

## When something is missing, say so in one line

- Nothing in the room: ask what the story is about, once.
- Key given, no tracker connection: create from what is in the room; the key is carried, the item unread.
- No tracker reachable at write time: the description in the room as markdown, and say the write was skipped.
- Item already complete: nothing to do.
