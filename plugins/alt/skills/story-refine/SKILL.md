---
name: story-refine
description: Creates a story in the tracker from an idea or a pasted draft, or refines an existing item into one the product owner can sign and a builder can challenge, saying what changes for whom, the rules it is accepted against, the examples at the edges, and what is still open and whose, never how. Use when the user wants a story, ticket, or issue written or refined, or invokes /alt:story-refine.
argument-hint: [key, pasted story, or the idea]
---

# story-refine

A story is what a team agrees to build, written so the product owner can sign it and the builder can challenge it. Every line says what changes for whom, states a rule the signer would reject the work over, shows an example at an edge, records a choice and why, or names a question and whose it is. None says how, and none says what the builder could read in the repo, run in the tests, or follow through a link. Refine it, show it, write it on the runner's go, then stop.

## Inputs

The seed is $ARGUMENTS or whatever is in the room: a key, a pasted story, an idea, the conversation so far. A key with a tracker connection means refine that item; anything else means create.

Preset: the `## Preset` heading of any `.agentic/alt/*/extend-skill.md`, else developer.

Read if present, ignore if absent: `.agentic/sources.md`, where this team's facts live, and `.agentic/alt/story-refine/extend-skill.md`, this repo's overrides under two headings. `## Preset`: one word. `## Shows`: the names of the fields the product shows a person as a headline, nothing else. Where the template, the extend file, and the preset disagree, the template rules, then the extend file, then the preset.

## Homework

Facts are looked up, never asked, and each is cited in the room by path and a symbol, heading, or quoted phrase, never a bare line number. That form is for the room; nothing written to the tracker cites a source.

- tracker: the item by key, its full thread, the parent the field names, and the parent's other open children by title and Open section; with no parent, the open items the seed or the thread links. A question a thread answered is not open. A question two siblings both carry is one question, owned once, on the story that lands first. Never search by text; offer the duplicate search in one line and run it only on a yes.
- code: the part the story names, one step out: what it calls, what calls it, the tests beside it. Rules and examples come from here, and so does the test of whether a line is derivable.
- docs: what covers that part, from the sources file and the item's links, what the product itself says about it, and the file that defines the product's words when the repo has one; the story is written in them, and a word it needs that the file lacks is either the how or a term the repo should define.
- people: never asked.

The homework shapes the story and catches false premises; none of it is written into the story or beside it. What the builder can look up, the builder looks up.

## Ask

One question a turn, only for what the room, the thread, and the code do not answer. In order: whose need this is and what they stop or start doing once it lands; what was seen, when, and in what words; the rules the product owner would reject the work over; the example at each edge the rules leave open; what a reader would assume is in and is not. Stop asking when the shape can be filled. A question with nobody in the room to answer it is an Open line, not a question.

## Then decisions

Invoke `alt:decisions` against the draft. Ask the runner each root, one a turn. An answer that changes what the person sees folds into a criterion or an example; an answer that only says why folds into Decided; `team` or no answer lands under Open with its hat, a name or `unassigned`, and its if-wrong line. A root about the need or the outcome belongs to the parent: with a parent it goes there and the story cites it; with none, the runner is offered `alt:epic-refine` once before the write, and a decline leaves the parent field empty with nothing said about why. If decisions did not load, Open reads `decisions did not run; run /alt:decisions on this story` and the closing line says so.

## Then the sweep

Five minutes on what else could be true: inputs the rules never mention, states the incident did not show, the case where the premise itself is false. Each hit is routed to a criterion, an example, Out of scope, or Open, and keeps its outcome on the way; when placing it would change what the person sees, it is an Open line. A hit that fits nowhere is an Open line, never dropped. The list itself is never written.

## Show, then write

Read `${CLAUDE_PLUGIN_ROOT}/skills/story-refine/template.md` only now. Fill it, then hold it against its own limits before showing: about 350 words; four sentences in the opener; three to six examples; at most three lines each under Decided and Open. Over a limit means split, or an Open line, never a rule trimmed to fit. A line that would be false after next week's commits goes; a line the builder could derive goes.

Show:

- On create: the title, the parent key or none, the keys it waits on, and the description.
- On refine, item already in the shape: each section where the item and this run disagree, both sides quoted; a line already there stays unless the runner says otherwise. An Open line the thread answered leaves Open and lands where its answer belongs.
- On refine, item not in the shape: a create from the need the item names; nothing in it is kept for being there, and the original stays in the item's edit history.

Then, in the room only, the Open lines that change what the person sees, since the story is not ready to pull until they close.

The tracker shows who wrote the story and when; the story does not repeat it. Ask once whether to create or edit it. On yes, write the title and parent to their fields, the description as one block, and each item this story waits on as the tracker's dependency relation, through whatever tracker the session reaches. A dependency the relation cannot hold, a pull request or a branch, is said in the room and written nowhere. Report the key. Then stop.

## Rules

- Data a rule turns on, a list, a map, a threshold, is the what: a short table on the story. A table too long for the story is a story too big.
- A line that changes what the person sees is a criterion or an example, wherever it started.
- Never a metric, a size, a priority, a status, or a readiness verdict on the story. Never a sentence telling the reader the story may be wrong.
- Never starts the work, never edits code, never enters plan mode.
- Written outside the session, to a tracker item or a message, a person is a name or handle and a role is the preset's word. The words the skills use for their own mechanics, runner, room, seat, hat, wound, shape, sweep, the record, never appear there.
- Non-interactive: every root lands under Open; show the draft and stop; the write needs the runner present.

## When something is missing, say so in one line

- Nothing in the room: ask what the story is about, once.
- Key given, no tracker connection: create from what is in the room; the key is carried, the item unread.
- No tracker reachable at write time: the description in the room as markdown, and say the write was skipped.
- No parent and the runner declines the epic: the parent field stays empty, and the need question is asked nowhere on the story.
- Item already complete: nothing to do.
- decisions did not load: the placeholder, and say so.
- Preset is business or research: developer work only, for now.
