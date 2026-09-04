---
name: examine
description: Round-based interview that surfaces the decisions hidden in a story, ticket, idea, or plan, asks nothing that can be looked up, and carries with each question what a wrong answer costs and who could help. Use only when the word "examine" appears ("let's examine that", "/alt:examine") or when another alt skill invokes it.
argument-hint: [preset] [ticket key, pasted story, or idea]
---

# examine

Interview the seed until nothing material is silently assumed. Facts are yours to find and are never asked. Decisions are a person's to make and are always asked, each carrying what it costs to get wrong and who could help answer it. The runner decides what they answer and what they hand to their team. The value is in surfacing what needs surfacing, and in showing plainly when something needs a team conversation rather than a quick patch to get the ticket done.

This is a grill, not a classroom. The reasoning behind a question travels with it in a line or two. Nothing lectures.

## Inputs

The seed is $ARGUMENTS, or whatever is in the room: a ticket key, a pasted story, an idea, the conversation so far. When a key is given and a tracker connection exists, read the ticket. Never re-ask what the conversation already answered.

Preset: if the first word of $ARGUMENTS names a file in `${CLAUDE_PLUGIN_ROOT}/presets/`, read it and drop the word from the seed. Otherwise use the preset named under a `## Preset` heading in the extension file. Otherwise the developer defaults below apply and nothing is read. A preset swaps the hats and the runner's default hat, where the record and facts usually live, the words for ready and for the small artifact, and any fixed string it renames. It never changes how the interview works.

Read if present, ignore if absent:
- `.agentic/sources.md`: where this team's facts live and who can reach them.
- `.agentic/alt/examine/extend-skill.md`: what only this repo knows, such as its hats, its record, and where approaches break here.

Developer defaults: the runner is Implementation Dev; the hats are Implementation Dev, Tech Leadership, Business, UX; the record is the ticket, the code beside the work, and the repo's docs; the small artifact is a spike or a prototype. State the assumed hat once, at the top of the first round, and accept a correction in plain speech.

On a re-run against a seed already examined, keep the question numbers, treat earlier answers as settled unless the runner reopens one, and say what closed.

## Facts are never questions

Read the files the work touches: code when there is code, otherwise the documents, notes, and data the seed is about. Read the ticket or record, the repo's docs, and every source the sources file names. Anything they answer is a fact. Look it up. Send a sub-agent whenever a lookup deserves one, and never hold a round for it: the questions that depend on the answer wait for a later round, the rest are asked now. Every fact you use says where it came from in a few words. A source that is listed but unreachable becomes one "look this up in X" line for the team.

## The tree, the frontier, the round

Map the seed as a design tree: every decision branches into the decisions that hang off it. The frontier is every decision whose prerequisites are settled, the questions that can be asked now without guessing at answers not yet given. Ask the whole frontier as one round, then wait. Answers settle decisions, the frontier moves outward, and the next round asks what that unblocked. Two questions never share a round if one depends on the other.

A wound is a premise the seed gets wrong or a decision it never made, with several questions hanging off it. Wounds are roots of the tree, so they come first on their own; there is nothing to announce. Hunt for them from six angles, run against the seed and never against the runner: feasibility, dependencies, edge cases, alternatives, scope and ordering, failure modes.

Before a candidate is asked, try to kill it. Is it a fact? Look it up; found means gone. Does the record settle it? Then it is one line with its source, shown on request, not a question. Should the thing forcing the decision exist at all? Removing the cause is the best answer. Only survivors are asked. There is no cap on how many that is and no kind of question that is off limits.

## A question

Each question carries the same parts in the same order. Real words, no severity labels; the if-wrong line is the severity.

```
❓ Q3  Retry the payment call, or make the enrollment recoverable?
Refinement notes say retry up to three times. Nothing in the story says what happens on the third failure, and the enrollment is already saved by then.

1. Record the payment as pending and reconcile later. Fixes the gap.
2. Retry three times and show the success page regardless. Defers the gap onto support.

➡️ Option 1. A member enrolled with no payment is the case the story is silent on, and it is the one Finance finds at month end.
If wrong: members enrolled without paying, or charged without enrolling.
To undo: a reconciliation job; hard once statements have gone out.
Could help: Tech Leadership, who own the recovery pattern for cross-service calls.
```

- Two or three genuine options, each tagged as fixing the problem or deferring it onto someone named. A quick patch is never shown as a peer of a fix.
- When a question needs a team conversation rather than a session answer, the recommendation says so and recommends sharing it, with the one line the runner would send. Anything touching money, legal, safety, or identity always takes that shape.
- When talking cannot settle a question because it needs something to react to, the recommendation is the small artifact: make it and come back.
- On a values or taste question the recommendation reads "given what you've said," never as a preference.
- Could help names the hat that holds the context, in this team's words, and why in a few words. It is help, not ownership; the runner may still answer.

## A round

Questions separated by a rule. The first round opens with one line: "Assuming you're Implementation Dev; say otherwise." Every round ends with the same ask:

```
Answer by number. "yes" takes every recommendation. "share 3" hands a question to the team. "more 3" goes deeper on one. "settled" shows what the record already decided. Or just tell me what's off.
```

No count of what is coming; the tree is not known until it is walked.

Read each answer against the record before it closes. An answer the record rules out gets one line naming the fact and stays open. Then recompute the frontier and say what moved, in one line:

```
That settled Q2 and Q5, retired Q7, and opened two new questions.
```

Numbers are stable and never reused. The interview ends when the frontier is empty, never when a list runs out.

## Close

Tally what happened, give one overall read, hand over the team list, and ask what next.

```
Decided: 6. Shared with the team: 3. Settled by the record: 4.
Read: ready with questions. The work can start; the shared items need answers before the payment call is wired.

Decided
- Q3 Record the payment as pending and reconcile later.
- Q4 Show the pending state on the success page.

For the team (copy and paste)
- For Tech Leadership: retry the payment call or make enrollment recoverable? If wrong: members enrolled without paying, found at month end.
- For Business: what does the member see while payment is pending? If wrong: support tickets on day one and no script to answer them.

Post these to PLAT-412? yes or no.
What next?
```

The overall read is one of: ready, ready with questions, conversation first, not workable. The preset may reword it. Every team bullet carries who it is for, in this team's words, and its if-wrong line, so the stakes cannot be shrunk on the way. Offer the post only when a record and a way to write to it exist; post only on yes. Then stop. Do not enter plan mode. Do not begin the work.

## When something is missing, one line at the moment it happens

- No code here: name the files you will read and ask once what else to read.
- No sources file: infer from the environment and say so.
- Source listed but unreachable: a look-this-up line for the team.
- No way to write to the record: the team list is the deliverable.

## Rules

- Never build, never enter plan mode, never act on an answer you were not given.
- Facts are never questions. Zero questions is a success; never invent one.
- A quick patch is never a peer of a fix.
- A preset changes words and defaults, never how the interview works.
- Plain speech always works. The last line of every round is the ask.
