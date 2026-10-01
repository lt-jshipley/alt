---
name: examine
description: Interview that surfaces the decisions in a story, ticket, idea, or plan, each with what a wrong answer costs and who could help, and asks nothing that can be looked up. Use only when the word "examine" appears ("let's examine that", "/alt:examine") or when another alt skill invokes it.
argument-hint: [ticket key, pasted story, or idea]
---

# examine

Interview the seed until nothing material is silently assumed. Facts are yours to find and are never asked. Decisions are a person's to make and are always asked, each carrying what it costs to get wrong and who could help answer it. The user decides what they answer and what they hand to their team. The reasoning behind a question travels with it in a line or two; nothing lectures.

## Inputs

The seed is $ARGUMENTS or whatever is in the conversation: a ticket key, a pasted story, an idea, the conversation so far. Read the ticket when a key and a tracker connection exist. Never re-ask what the conversation already answered.

Read if present, ignore if absent: the `## alt` section of the repo's CLAUDE.md, its `Tracker:` and `Docs:` lines, for where facts live. Absent, the tracker is whatever tracker tool the session reaches and the docs are README and `docs/`.

Re-run on the same seed: keep the numbers, earlier answers stay settled unless reopened, say what closed.

## Roles

Who could help is one of four: Product Owner, Tech Lead, Engineer, Designer. Could help is help, not ownership. Anything touching money, legal, safety, or identity is a team conversation, never one person's answer. A call across a service or team boundary names the Tech Lead even when the developer could answer.

## Facts are never questions

Read what the work touches, the ticket and its thread, and the docs. Anything they answer is a fact; look it up and say where it came from in a few words. Send a sub-agent whenever a lookup deserves one and never hold the interview for it: a question that depends on the answer waits its turn. Zero questions is a success; never invent one.

## The tree, the frontier, the turn

Map the seed as a design tree: every decision branches into the decisions that hang off it. The frontier is every decision whose prerequisites are settled. Ask one question from the frontier, then wait. Next is a child of what was just answered when one is on the frontier, else the frontier question whose if-wrong line costs most.

A root is a premise the seed gets wrong or a decision it never made, with several questions hanging off it. Roots come first. Hunt from six angles, against the seed and never the user: feasibility, dependencies, edge cases, alternatives, scope and ordering, failure modes.

Before a candidate is asked, try to kill it. Does the ticket thread or the code settle it? Then it is one line with its source, shown on request. Should the thing forcing the decision exist at all? Removing the cause is the best answer. Only survivors are asked, with no cap on count or kind.

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
Could help: <role>, <why they hold the context>
```

- A quick patch is never a peer of a fix.
- When a question needs a team conversation, the recommendation says so and drafts the line to send. Money, legal, safety, and identity always go to the team that way.
- When a question needs something to react to, the recommendation is a spike or a prototype: make it and come back.
- On a values or taste question the recommendation reads "given what you've said," never as a preference.

## A turn

Nothing renders before the first question, and nothing announces what is coming. Between questions, one line: what settled, retired, and opened, and how many are open. Every turn ends with the same ask:

```
Answer by number, or "yes" for the recommendation. "share" sends it to the team, "more" goes deeper, "settled" shows what the ticket and the code already decided. Or tell me what's off.
```

Read the answer against the ticket and the code before the question closes; one they rule out gets one line naming the fact and stays open. Never act on an answer you were not given. Numbers are stable and never reused. The interview ends when the frontier is empty, never when a list runs out.

## Close

```
Decided: <count>. Shared with the team: <count>. Settled by the ticket and the code: <count>.
Read: <ready, ready with questions, conversation first, or not workable>. <what can start now; what waits on the team>

Decided
- Q3 <the decision, plainly>

For the team (copy and paste)
- For <role>: <the question>. If wrong: <what breaks, for whom>

These go on the ticket; paste them there.
What next?
```

Ready with questions means the work can start and the open items land before it merges. Team bullets keep their if-wrong lines so the stakes cannot be shrunk on the way. Recommend the paste; never post. Then stop. Never build, never enter plan mode.

## When something is missing, say so in one line

- Nothing to read yet: name what you will read and ask once what else.
- A source CLAUDE.md names but this session cannot reach: a look-this-up line for the team.
