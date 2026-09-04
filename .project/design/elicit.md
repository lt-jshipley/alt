# elicit: high-level design, first version

Draft for review, 2026-09-03. One skill, `alt:elicit`. The research behind every choice here is in `.project/research/agentic-skills/grill-me.md`. This doc says what the first version does, what it deliberately does not do, and what is open for you to decide.

## What it is for

A pre-work interview that holds the fact-versus-decision line for the person running it, asks them only what is theirs to decide and cheap to get wrong, and hands everything else to its owner in a form that carries its stakes. It teaches as it goes, because in this era guards are brittle and teaching is what holds.

The measure of a run is how few decisions the runner had to make, that none of them could hurt, and that what was not theirs left the session in a shape the team could act on. Fewer is about what reaches the runner as a decision. Coverage is not reduced: every branch is visited and nothing is silently assumed, however many questions that takes.

## Who it is written for

The person actually at the keyboard, who is often not the owner of the answers, not a reliable courier to those owners, and not equipped to tell a fact from a decision. There is one presentation and it is for that person. There is no senior mode. Anyone who wants it different prompts around it or overrides it in the extension file.

It is a grill, not a classroom. The reasoning behind a question travels with it so the runner understands why it is being asked and why it is or is not theirs. Nothing lectures, nothing teaches the profession, and no line exists only to instruct.

## First-version scope

Engineering stays low. What is in:

- One skill file, `plugins/alt/skills/elicit/SKILL.md`. Model-invocable so other alt skills and workflows can call it, with a description that triggers only on the literal word "elicit" and refuses paraphrases such as "what am I not deciding." No passthroughs yet.
- Reads two optional files if present, ignores them if absent: `.agentic/sources.md` for where facts live, and `.agentic/alt/elicit/extend-skill.md` for what only this repo knows. No sync, no stubs, no seed file for the runner.
- Text output only. No popup, no adapters, no persistence beyond the team list and an offered ticket comment.
- Tested by running it on real stories and recording what it did wrong in the research doc.

What is out, with the reason:

- Passthroughs `grill-me` and `socrates`. Earn the abstraction: one consumer today.
- Delivery adapters per tracker. Most work in the design, and the first version should prove the interview before we build the pipe.
- A runner seed file. Role and seniority have no agreed home yet. The default presentation covers the person least served by other tools.
- Per-question sub-agent refute passes. Inline first. Add sub-agents when the lookup is wide, as Matt does.
- The eval harness. Gated for the organisation. Cases are written by hand and run by hand.
- Stance derivation and the retro loop. The record in a fresh shop is code neighbours, the ticket, and the docs. That is enough to settle a lot.

## The run

### 0. Ingest

Take what is in the room: a ticket key or pasted ticket, a story, an idea, or the conversation so far. If a tracker connection exists and a key is given, read the ticket. Never re-ask what the conversation already answered. On a re-run against the same seed, carry forward question ids and treat prior dispositions as settled unless reopened.

### 1. Homework

Facts are never questions. Read the files the work touches, code when there is code and otherwise the documents, notes, and data the seed is about, plus the ticket or record, the repo's docs, and whatever `.agentic/sources.md` names. Every fact the skill uses carries where it came from, in a few words. Dispatch a sub-agent only when the lookup is wide. When a source is listed and unreachable, say so once and turn the fact into a look-this-up line for the team.

When there is no code, name the files that will be read and ask once what else to read. Then proceed. Anyone in Claude Code has artifacts; the question is what kind and where.

### 2. Hunt

Two hunts. What the seed leaves ambiguous, and where the proposed approach breaks. The break hunt runs six angles against the seed, never against the runner: feasibility, dependencies, edge cases, alternatives, scope and ordering, failure modes. A flaw found is a candidate decision like any other.

### 3. Refute

Every candidate question gets a targeted attempt to kill it before it can reach a person, in this order:

- Is it a fact? Look it up now. If found, it is gone.
- Does the record settle it? The code beside the work, the ticket's constraints, the docs. If so, show it settled with its source. No card.
- Should the thing forcing the decision exist at all? Removing the cause is the best disposition.
- Is a wrong pick cheap to undo and is it the runner's to make? Then it is the runner's.
- Otherwise it belongs to someone else.

Only survivors become questions. This is the pass that examine specified at triage and that only held when run as a separate challenge. Here it is not optional.

### 4. Group and grade

Group surviving questions by the wound they are symptoms of, not by owner or by seam. Attach to each question three lines, one each: if wrong, to undo, you'd know it was wrong if. Concrete or omitted. No severity words.

Assign each question to a hat. The default list for development work is Implementation Dev, Tech Leadership, Business, and UX. The runner is whichever of these they are, and a question is theirs only when it belongs to their hat and a wrong pick is cheap. The extension file may rename, add, or remove hats. Questions touching money, legal, safety, or identity are routed to their hat and never batched, whatever the hat is.

A question gates work only when all three hold: the record is silent, a wrong pick is expensive to undo, and it is not the runner's. A gate must also name a concrete harm from proceeding now. Without one it is downgraded to a question. Gates should be zero or one. More is a smell on the classifier, and it reclassifies before presenting.

The verdict is one of four: ready, ready with questions, conversation first, not workable. Most runs should land on ready with questions. A preset may reword ready, for example ready to run.

### 5. First screen

Twenty lines or fewer. Verdict and counts on line one. Wounds next, at most three, three lines each: what it is plainly, the harm if built now, who owns it. Then the runner's pile as a one-line index with the recommended answer marked. Then one ask with a default.

Nothing renders above the verdict. No preamble, no summary of what is about to happen.

When the verdict is conversation first, there is no "you can proceed on" line. The next action is the conversation, the message is drafted, and the screen says so. A runner who wants the partition asks for it in plain language, and it is given with the gate still named.

### 6. Walk

One question per screen, inside a named wound group. A breadcrumb at the top says in plain words what is still coming and that the team message comes after. Remaining count, never a total.

Each question shows: the decision in plain words, the mechanism in two or three lines, the three consequence lines, two or three genuine options each tagged as fixing the problem or deferring it onto someone, the recommended one marked with its why. A patch never appears as a peer. The last line is always: answer by number, yes for the recommendation, or tell me what's off.

Answers are read against the record before the question closes. An answer the record rules out is said so in one line and the question stays open. After each answer, deltas only: what was added, what was retired, the breadcrumb updated. Ids are stable and never reused.

Questions that are not the runner's are not walked. They are shown once, on the first screen as wounds or at the end in the team list, with one line of reasoning: why this is not yours.

**The walk is living.** Re-deriving after every answer is the engine of the walk, not a display rule.

- An answer can spawn questions, retire them, move one to a different wound group, change who owns it, change the verdict, or open a gate that was not there. All of these are shown as one-line deltas.
- A question whose answer depends on one still open waits. The breadcrumb reflects that some of what is coming does not exist yet.
- The walk ends when nothing material remains, never when the original list runs out.
- Question count is not capped. A story that needs forty questions gets forty. The caps in this design are on gates, on lines per screen, and on options per card, never on how many questions are asked.
- Later screens may be longer than they looked, not only shorter. An answer that reveals the story is bigger than it seemed grows the walk, and the breadcrumb says so in one line.

### 7. Close

- What the runner decided, one line each.
- The team list: copy-pasteable bullets for everything that is not the runner's. Each bullet carries who it is for, in the team's words, and its if-wrong line. Full context travels with the question so it cannot be shrunk on the way.
- If a record exists and there is a way to write to it: ask to post the list there. Post only on yes. The developer default record is the ticket.
- One handoff line stating what is ready to proceed and what waits on the team. No automatic entry into plan mode.

The skill never acts on an answer it was not given, never proceeds past an unanswered gate, and never starts building.

## Presentation rules

- Fixed shapes, same blocks in the same order every render.
- Budgets checked, not felt: first screen twenty lines, a wound three, a card twelve plus its mechanism.
- Plain labels. "If wrong," "to undo," not blast radius.
- One ask per turn, one default, plain-speech exit.
- Three verbs: a number or yes, not mine, more. Anything else is plain speech, and the skill honours it.
- Deltas, never re-renders.

## Reasoning travels, lightly

- Every routed question carries one line on why it is not the runner's.
- Every fact carries where it came from, in a few words.
- Every refusal to proceed explains itself in the same breath, in one line.
- The message to the team is written for the runner so that sending it is the cheapest move available.
- No line exists only to teach. If a line does not help the runner answer or route the question in front of them, it is cut.

## Degradation, stated in one line each at the moment it happens

- No code here: name the files that will be read, ask once what else to read.
- No way to write to the record: the team list is the deliverable.
- No sources file: infer from the environment and state the assumption.
- Source listed but unreachable: a look-this-up bullet for the team.
- Runner contests a gate: proceed on their word and record the reason in the close.

## Budget

- Description: one sentence with a use-when clause.
- On-invoke: the whole skill under roughly three thousand tokens. No unconditional reference file.

## How we will know

Run it on three real stories: one that is clean, one with a structural wound, one from a non-developer with no repo. Record in the research doc:

- Fact questions that reached the runner. Target zero.
- Gates raised and whether the team agreed each was real.
- Line counts of the first screen and of each card.
- Whether the team list was sent unchanged.
- Where the runner said "tell me what's off" and why.

## Decisions

All eight reviewed and decided 2026-09-03.

1. **Invocation. Decided 2026-09-03.** Model-invocable, because the user-only flag also blocks the Skill tool and other skills and workflows will call this. The description triggers on the literal word "elicit" only, so "let's elicit that" fires it and "what am I not deciding" does not. Something outside the skill still has to tell a junior when to run it.
2. **Presentation. Decided 2026-09-03.** One presentation, written for the junior, no senior mode. Reasoning travels with each question at a light-to-normal level, because carrying the why is how understanding happens, but it is a grill, not a classroom. Overrides come from prompting or the extension file.
3. **File layout. Decided 2026-09-03.** One file. Everything in SKILL.md under roughly three thousand tokens. If the shapes push it over budget, that is a signal to cut, not to split.
4. **Extension files. Decided 2026-09-03.** Read `.agentic/sources.md` and `.agentic/alt/elicit/extend-skill.md` when present, ignore when absent. Zero cost when absent, and the test stories exercise the extension idea early. Headings in both are provisional until the shared-extension design is decided.
5. **Input. Decided 2026-09-03.** Text. Answer by number, yes, or plain speech. Works in every harness and keeps the screen and the answer together. The popup stays a future experiment.
6. **Handoff. Decided 2026-09-03.** State it and stop. One line on what is ready to plan and what waits on the team. Nothing entered automatically, so elicit stays usable from other skills that have their own next step.
7. **Hat names. Decided 2026-09-03.** The skill supplies a default list and the extension file overrides it. Default for development: Implementation Dev, Tech Leadership, Business, UX. Money, legal, safety, and identity are a never-batched rule on top of whichever hat owns them, not a hat of their own. The list itself now comes from the preset; see decision 9.
8. **Settled by the record. Decided 2026-09-03.** Yes, in the first version, with code neighbours, ticket constraints, and the repo's docs as the record. A decision they settle is shown in one line with its source and never becomes a question. Stances, if alt adopts any, widen the record later.
9. **Presets. Decided 2026-09-03.** Every persistent failure on non-development seeds shared one root: the skill carried a developer's world in its defaults and fixed strings. A preset is a one-screen file that swaps only the hats and the runner's default hat, where the record and facts usually live, the words for ready and for the small ungrillable artifact, and named fixed strings. Developer is the inline default and costs no read. Business and research ship as files. Selected by the first word of the arguments, or by a `## Preset` heading in the extension file so nobody types it twice. A preset never changes the mechanics. Alongside it: the ungrillable rule the design named but the skill text had not carried, neutral wording (if done now, ready to proceed, the record, not workable), and one line on values or taste questions where the recommendation reads "given what you've said" rather than as a preference.

## Calls made while writing

Recorded 2026-09-03, when the design became a skill file. Small decisions the design left open, made to stay consistent with the eight above.

1. The description is positive-only. Refused phrases such as "what am I not deciding" and "grill me" are tested for, not listed, because naming them in always-on text risks attracting them.
2. The runner's hat comes from the preset, Implementation Dev by default, stated on the first screen when assumed, and correctable in plain speech. This replaced the repo-or-not inference on 2026-09-03; "Business when there is no repo" was wrong for a novelist, a researcher, and most non-developers.
3. Settled entries render as one count line on the first screen, expanded on "settled."
4. Routed questions that are not gates are counted on line one and listed in the close.
5. More than three wounds: three shown, highest harm first, then "N more after these."
6. Not a story gets one screen, no walk, and the team list is still offered.
7. A re-run's comment names the one it supersedes and lists what closed.
8. A ticket named mid-walk is read then and reconciled as a re-run.
9. The ➡️ glyph marks the recommendation, matching the reviewed mocks.
