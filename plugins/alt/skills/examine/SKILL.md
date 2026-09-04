---
name: examine
description: Interview that surfaces the decisions in a story, ticket, idea, or plan, each with what a wrong answer costs and who could help, and asks nothing that can be looked up. Use only when the word "examine" appears ("let's examine that", "/alt:examine") or when another alt skill invokes it.
argument-hint: [preset] [ticket key, pasted story, or idea]
---

# examine

Interview the seed until nothing material is silently assumed. Facts are yours to find and are never asked. Decisions are a person's to make and are always asked, each carrying what it costs to get wrong and who could help answer it. The runner decides what they answer and what they hand to their team. The reasoning behind a question travels with it in a line or two; nothing lectures.

## Inputs

The seed is $ARGUMENTS or whatever is in the room: a ticket key, a pasted story, an idea, the conversation so far. Read the ticket when a key and a tracker connection exist. Never re-ask what the conversation already answered.

Preset: the first word of $ARGUMENTS if it names a file in `${CLAUDE_PLUGIN_ROOT}/presets/`, else the `## Preset` heading of the extension file, else `developer.md`. Drop the word from the seed. A preset names the kind of work, never the person, and never changes how the interview works.

Read if present, ignore if absent: `.agentic/sources.md`, where this team's facts live and who can reach them, and `.agentic/alt/examine/extend-skill.md`, this repo's hats, record, and where approaches break here.

Re-run on the same seed: keep the numbers, earlier answers stay settled unless reopened, say what closed.

## Facts are never questions

Read what the work touches, the record, and every source the sources file and preset name. Anything they answer is a fact; look it up and say where it came from in a few words. Send a sub-agent whenever a lookup deserves one and never hold a round for it: only the questions that depend on the answer wait. Zero questions is a success; never invent one.

## The tree, the frontier, the round

Map the seed as a design tree: every decision branches into the decisions that hang off it. The frontier is every decision whose prerequisites are settled. Ask the whole frontier as one round, then wait. Two questions never share a round if one depends on the other.

A wound is a premise the seed gets wrong or a decision it never made, with several questions hanging off it. Wounds are roots, so they come first on their own. Hunt from six angles, against the seed and never the runner: feasibility, dependencies, edge cases, alternatives, scope and ordering, failure modes.

Before a candidate is asked, try to kill it. Does the record settle it? Then it is one line with its source, shown on request. Should the thing forcing the decision exist at all? Removing the cause is the best answer. Only survivors are asked, with no cap on count or kind.

## A question

No severity labels; the if-wrong line is the severity.

```
❓ Q3  <the decision, as a question in plain words>
<why the seed does not settle it, two or three lines>

1. <option>. Fixes <what>.
2. <option>. Defers <what> onto <whom>.

➡️ <recommended option, and why in one clause>
If wrong: <what breaks, for whom>
To undo: <the move, and when it gets hard>
Could help: <hat>, <why they hold the context>
```

- A quick patch is never a peer of a fix.
- When a question needs a team conversation, the recommendation says so and drafts the line to send. Money, legal, safety, and identity always take that shape.
- When a question needs something to react to, the recommendation is the small artifact: make it and come back.
- On a values or taste question the recommendation reads "given what you've said," never as a preference.
- Could help is help, not ownership.

## A round

Questions separated by a rule. Nothing renders above the first question and nothing announces what is coming. Every round ends with the same ask:

```
Answer by number, or "yes" for every recommendation. "share 3" sends one to the team, "more 3" goes deeper, "settled" shows what the record decided. Or tell me what's off.
```

Read each answer against the record before it closes; one the record rules out gets one line naming the fact and stays open. Never act on an answer you were not given. Then recompute the frontier and say in one line what settled, retired, and opened. Numbers are stable and never reused. The interview ends when the frontier is empty, never when a list runs out.

## Close

```
Decided: <count>. Shared with the team: <count>. Settled by the record: <count>.
Read: <ready, ready with questions, conversation first, or not workable>. <what can start now; what waits on the team>

Decided
- Q3 <the decision, plainly>

For the team (copy and paste)
- For <hat>: <the question>. If wrong: <what breaks, for whom>

Post these to <the record>? yes or no.
What next?
```

Team bullets keep their if-wrong lines so the stakes cannot be shrunk on the way. Offer the post only when a record and a way to write to it exist; post only on yes. Then stop. Never build, never enter plan mode.

## When something is missing, say so in one line

- Nothing to read yet: name what you will read and ask once what else.
- Preset cannot be read: ask which kind of work this is.
- Source listed but unreachable: a look-this-up line for the team.
