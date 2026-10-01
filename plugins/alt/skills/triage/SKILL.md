---
name: triage
description: Reads a scope of open work, an epic and its children, a board's active cut, or a story's parent, and says what its symptoms are symptoms of. Fixes what the tickets already settle, routes what nobody holds as an Open line to the holder, names what is holding. Never grades an item or orders the work. Use when the user asks to triage, asks what is wrong with a backlog or an epic, or invokes /alt:triage.
argument-hint: [epic key, story key, project or board, or nothing]
---

# triage

A count is a symptom. Triage reads a scope of open work in full, names the mechanism behind each count and who holds it, fixes what the tickets already settle, names what is holding, and writes on the user's go. It never grades an item and never orders the work; those are the team's.

## Inputs

The seed is $ARGUMENTS or what is in the conversation. An epic key: the epic and its children. A story key: its parent's scope; with no parent, the project's parentless stories, which is the symptom itself. A project or board: the tracker's own active cut when it has one, sprint, iteration, or columns, else in progress at any age plus anything touched in the last month. The older tail is counted and dated, never read, and offered as a second run. Nothing named: ask once.

The window is the last month, or the active cut's length when the tracker has one.

Read if present, ignore if absent: the `## alt` section of the repo's CLAUDE.md, its `Tracker:`, `Measures:`, and `Docs:` lines. Absent, the tracker is whatever tracker tool the session reaches, there are no measures, and the docs are README and `docs/`.

## Homework

Facts are looked up, never asked, and each is cited in a few words. Declare the denominator before reading: items in scope, items in the tail.

- tracker: every item in scope in full: fields, description, the whole thread, parent and child links. A question the thread answered is not open. Never search by text. A scope too large for one read fans out to sub-agents, one set of items each, returning per item its symptoms, what its thread settles, and which Open lines are still open.
- measures: the `Measures:` line, for the baseline of any epic whose Outcome line reads unmeasured.
- docs: what the items link. Read only where a symptom points there.
- code: none.
- people: never asked.

## Sort

Symptoms are what the lt-backlog story and epic skills leave on the tickets on purpose: a story with no parent; a story whose Open routes to `Parent: none`; an epic unmeasured with children in progress; a title-only epic with children; a child whose title does not serve its epic's need; an Open line untouched for the window; a `Not yet a story` piece that has a child; a description its thread contradicts. Each is sorted once.

- **A fact.** The tickets settle it: a parent the thread names by key, a baseline the thread or the `Measures:` line holds, an Open line the thread answered, a `Not yet a story` piece whose story is already the epic's child. It becomes a fix, one edit, in the same form as its sibling items. However many there are, facts are never a cause.
- **A cause.** Symptoms across items sharing one cause that is a decision nobody holds: a need, a measure, or what hangs under what. One Open line on the shared parent, holder's role and name, if-wrong, the symptoms as evidence. Causes are ordered by how many symptoms each dissolves.
- **A one-off.** A decision on one item, the target for a baseline the thread gave being the common one. One Open line on that item, shown under Open.
- **Fine.** Nothing written.

The epic format is the one lt-backlog's epic-create writes: a need, an Outcome line, a Bet, who holds what, and Open. Where a cause's line lands: a parent in that format gets it under Open. A parent not in that format gets it as one comment in the same wording, never a rewrite; the report names `/lt-backlog:epic-create` for that item. No parent means the line is a message to the holder, shown after the causes, and nothing is written. A no-parent cause is held by the Tech Lead; a name only when the thread gives one.

Roles are four: Product Owner, Tech Lead, Engineer, Designer.

## Show, then write

Read `${CLAUDE_PLUGIN_ROOT}/skills/triage/template.md` only now. Fill it; nothing renders before its header. Show the report, then the batch: every write by key, Open line, comment, or field, with the line as it will land. Ask once whether to write. On yes, write through whatever tracker the session reaches and report the keys. Then stop.

## Rules

- Every line of the report names a mechanism, names who holds it, or fixes a fact. The header is the denominator. Never a verdict on an item, a severity label, a score, an order of work, a count under no cause, or a sentence about a person.
- One yes per run covers the Open lines, comments, and field fixes together.
- A line already in an item stays. An Open line triage wrote before and still open is not written again; one the thread has since answered is a fix.
- A parent is set only when the thread names it by key; a placeholder line that matches a story's title is a one-off Open line for the epic's decision holder, not a fact. Never creates an item, chooses a parent, moves, closes, or reprioritizes anything.
- Never starts the work, never edits code, never enters plan mode, never invokes another skill; recommends the lt-backlog story or epic skill in one line.
- In anything written to a ticket, a comment, or a message, a person is a name or handle and a role is one of the four.
- Non-interactive: show the report and stop; the write needs the user present.

## When something is missing, say so in one line

- Nothing named and nothing in the conversation: ask what scope to read, once.
- Key given, no tracker connection: nothing to read; say so and stop. Items pasted in the conversation are sorted as pasted, never called a scope.
- Scope empty: nothing to do.
- Nothing wrong: the header and what is holding, then stop. Zero findings is a success.
- Tail larger than the scope: the header says so, and the second run is offered.
- No tracker reachable at write time: the batch as markdown in the conversation, and say the write was skipped.
- No `Measures:` line and an epic still unmeasured after the read: say `CLAUDE.md has no Measures line under ## alt; add one when a number exists`, once.
