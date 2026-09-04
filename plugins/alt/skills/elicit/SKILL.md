---
name: elicit
description: Interview that surfaces the decisions hidden in a story, ticket, idea, or plan, asks the runner only what is theirs, and routes the rest to its owner. Use only when the word "elicit" appears ("let's elicit that", "/alt:elicit") or when another alt skill invokes it.
argument-hint: [preset] [ticket key, pasted story, or idea]
---

# elicit

Interview the seed until nothing material is silently assumed. Hold the line between what can be looked up and what must be decided: facts are yours to find, decisions are a person's to make. Ask the runner only what is theirs to decide and cheap to get wrong. Everything else leaves the session addressed to its owner, carrying its stakes.

The measure of a run: how few decisions the runner had to make, that none of them could hurt, and that the team can act on the rest. Coverage is never reduced to get there; every branch is visited, however many questions that takes. This is a grill, not a classroom. The reasoning behind a question travels with it. Nothing lectures.

## Inputs

The seed is $ARGUMENTS, or whatever is in the room: a ticket key, a pasted story, an idea, the conversation so far. When a key is given and a tracker connection exists, read the ticket. Never re-ask what the conversation already answered.

Preset: if the first word of $ARGUMENTS names a file in `${CLAUDE_PLUGIN_ROOT}/skills/elicit/presets/`, read that file and drop the word from the seed. Otherwise use the preset the extension file names under a `## Preset` heading. Otherwise the developer defaults in this file apply and nothing is read. A preset swaps only the hats and the runner's default hat, where the record and facts usually live, the words for ready and for the small artifact, and any fixed string its Words heading renames. It never changes the mechanics.

Read if present, ignore if absent:
- `.agentic/sources.md`: where this team's facts live and who can reach them.
- `.agentic/alt/elicit/extend-skill.md`: what only this repo knows, such as its hats, its record, and where approaches break here.

The runner's hat: the preset's runner hat, Implementation Dev by default, unless the extension file or the runner says otherwise. When assumed, state it on the first screen and accept a correction in plain speech.

Re-run against a seed already elicited: carry the Q ids forward, treat prior dispositions as settled unless the runner reopens one, and note what closed.

## Homework: facts are never questions

Read the files the work touches: code when there is code, otherwise the documents, notes, and data the seed is about. Read the ticket or record, the repo's docs, every source the sources file names, and whatever the preset says people in this kind of work usually keep. Anything they answer is a fact: look it up, never ask it. Every fact you use names where it came from in a few words. Dispatch a sub-agent only when a lookup is wide. A source that is listed but unreachable becomes a "look this up in X" line for the team, said once.

No code here: name the files you will read, ask once what else to read, then proceed.

## Hunt

Two hunts. First, what the seed leaves ambiguous. Second, where the proposed approach breaks: run six angles against the seed, never against the runner. Feasibility, dependencies, edge cases, alternatives, scope and ordering, failure modes. A flaw found is a candidate decision like any other.

## Refute, in this order

Every candidate gets a targeted attempt to kill it before it can reach a person.

1. Is it a fact? Look it up now. Found means gone.
2. Does the record settle it? The code beside the work, the ticket's constraints, the docs. Settled means one line with its source and no question.
3. Should the thing forcing the decision exist at all? Removing the cause is the best disposition.
4. Is a wrong pick cheap to undo, and is it the runner's hat? Then it is the runner's.
5. Otherwise it belongs to another hat.

Only survivors become questions.

A survivor that talking cannot settle, because it needs something to react to, is not asked. It becomes one line: make the small artifact and come back. Developer default: a spike or a prototype; the preset names its own.

## Group and grade

Group survivors by the wound they are symptoms of, not by owner or by seam. A wound is a premise the seed gets wrong or a decision it never made, with several questions hanging off it. One small question is not a wound. When nothing is structurally wrong there are no wounds, and the questions are listed plainly. Each question carries three lines, one each, concrete or omitted, never a severity word:

- If wrong: what breaks, for whom.
- To undo: the move.
- You'd know if: the signal.

Hats come from the preset. Developer default: Implementation Dev, Tech Leadership, Business, UX. The extension file may rename, add, or remove. One owner per question; when a hat is not on the list, name it and say it is a guess. A question is the runner's only when it belongs to their hat and a wrong pick is cheap. Anything touching money, legal, safety, or identity is routed to its hat and never batched.

A gate is a question that meets all four: the record is silent, a wrong pick is expensive to undo, it is not the runner's, and a concrete harm from proceeding now is named. Missing any one, it is a question, not a gate. Expect zero or one gate. More is a smell on the classifier; reclassify before presenting.

Verdict, one of four: ready, ready with questions, conversation first, not workable. Most runs land on ready with questions. The preset may reword ready, for example ready to run.

## First screen

Twenty lines or fewer, degradation lines included; when more than one applies, combine them into one line. Nothing renders above the verdict line: no preamble, no summary of what is coming. The fences in this file show shape only; render every screen as plain text, never inside a code block.

```
<Verdict>. <N> wounds, <M> questions: <a> yours, <b> for the team. Assuming you're <hat>; say otherwise.

W1  <the wound, plainly>
    If done now: <what breaks, for whom>
    Owner: <hat>. Message drafted.

Yours (answer by number, or "all yes"):
  Q2  <question>                          ➡️ <recommended>
  Q4  <question>                          ➡️ <recommended>

Start with yours? I'll take them one at a time, then we send the team message.
yes, or tell me what's off.
```

- Wounds: at most three, highest harm first, then one line "N more after these."
- Settled entries: one count line, "N settled by the record. Say settled to see them."
- Routed questions that are not gates: counted on line one, listed in the close.
- Conversation first: no "you can proceed on" line. The gate is named on its wound and the message is drafted. The runner's pile is still listed and still walked, so they reach the conversation with their own decisions made. The ask does not change.
- Not workable: one screen, why and what would make it workable, no walk, team list still offered.

## Question screen

Show the group header once, then one question per screen.

```
Still coming: <plain words>, then <plain words>. Then the team message.

Q4  <the decision, plainly>
    <mechanism: what is ambiguous and why the seed does not settle it, two or three lines>

    If wrong: <what breaks, for whom>
    To undo: <one move>
    You'd know if: <the signal>

    1. <option>, fixes <what>          ➡️ recommended: <why, one clause>
    2. <option>, defers <what> onto <whom>

Answer 1 or 2, yes for the recommendation, or tell me what's off.
```

Breadcrumb in plain words, remaining never a total, the team message always last. Two or three options, each tagged fixes or defers onto whom. A patch never appears as a peer of a fix. On a values or taste question the recommendation reads "given what you've said," never as a preference. The last line is always the ask, in that shape.

## After an answer: the walk is living

Read the answer against the record before the question closes. An answer the record rules out gets one line naming the fact that rules it out, and the question stays open.

Then re-derive. An answer can spawn questions, retire them, move one to another wound group, change who owns it, change the verdict, or open a gate. Show only deltas:

```
Q4: <answer>. That removed Q7. That added one: Q9, <plain words>.
Still coming: <updated>.
```

A question whose answer depends on one still open waits its turn. Ids are stable; a retired id is never reused. Later screens may be longer than they looked; say so in one line. When a group ends, one line closes it. The walk ends when nothing material remains, never when the original list runs out. Question count is not capped; the caps are on screens.

A ticket or record named mid-walk is read then and reconciled as a re-run. A question that turns ungrillable mid-walk gets the small-artifact line and is parked, not asked.

## Close

```
Decided:
- Q2 <question>: <answer>

For the team (copy and paste):
- For <hat>: <question>. If wrong: <harm>

Post these to <record>? yes, or no.
Ready to proceed: <what>. Waits on the team: <what>.
```

Every team bullet carries who it is for, in this team's words, and its if-wrong line, so it cannot be shrunk on the way. Offer the post only when a record and a way to write to it exist; the developer default record is the ticket. Post only on yes. On a re-run, the comment names the one it supersedes and lists what closed. Then stop. Do not enter plan mode. Do not begin the work.

## Degradation, one line each, at the moment it happens

- No code here: name the files you will read, ask once what else to read.
- No way to write to the record: the team list is the deliverable.
- No sources file: infer from the environment and state the assumption.
- Source listed but unreachable: a look-this-up bullet for the team.
- Runner contests a gate: proceed on their word and record the reason in the close.

## Rules

- Never build. Never enter plan mode. Never proceed past an unanswered gate.
- Never act on an answer you were not given.
- Facts are never questions. Zero questions is a success; never invent one.
- No severity words. The if-wrong line is the severity.
- A patch is never a peer of a fix.
- Nothing renders above the verdict.
- A preset changes words and defaults, never the mechanics.
- Three verbs and no others advertised: a number or yes answers; "not mine Qn" sends it to the team list; "more Qn" expands to half a screen. Plain speech is honoured. The last line of every screen is the fixed ask, whatever the verdict.
- A routed question carries one line on why it is not the runner's. No line exists only to teach.
